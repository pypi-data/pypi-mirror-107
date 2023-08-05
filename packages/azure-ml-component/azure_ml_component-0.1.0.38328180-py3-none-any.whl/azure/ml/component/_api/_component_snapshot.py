# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import multiprocessing
import os
import tempfile
import zipfile
import ruamel
import logging
from typing import Optional
from shutil import copytree
from pathlib import Path

from azureml._common.async_utils import TaskQueue
from azureml.exceptions import UserErrorException
from azureml._project.ignore_file import get_project_ignore_file, IgnoreFile
from azure.ml.component._util._loggerfactory import _LoggerFactory
from azure.ml.component._util._utils import _copy2, TimerContext, _relative_to
from azure.ml.component._api._snapshots_client_core import AZUREML_SNAPSHOT_DEFAULT_TIMEOUT
from azure.ml.component._api._utils import try_to_get_value_from_multiple_key_paths, get_value_by_key_path, \
    _make_zipfile, is_absolute, create_or_cleanup_folder, check_spec_file, _looks_like_a_url

COMPONENT_SNAPSHOT_DIR_NAME = ".build"
FILE_HINT_IN_YAML = 'file:'


def _get_default_property(property_name):
    """
    Copied from azureml._base_sdk_common.cli_wrapper._common.get_default_property to decouple aml cli dependency.
    :return: Returns the default property value for property_name, if set using "az configure" command.
    Return None if no default value found.
    :rtype: str
    """
    try:  # python 3
        from configparser import ConfigParser
    except ImportError:  # python 2
        from ConfigParser import ConfigParser
    config = ConfigParser()
    # we always use az ml, so the config folder is .azure
    config_folder = ".azure"
    config.read(os.path.expanduser(os.path.join('~', config_folder, 'config')))
    if not config.has_section('defaults'):
        return None

    if config.has_option('defaults', property_name):
        return config.get('defaults', property_name)
    else:
        return None


class SnapshotItem:
    def __init__(self, absolute_path, *, relative_path_in_snapshot=None):
        self._absolute_path = absolute_path.resolve()

        # This check can NOT be removed.
        # Since the incoming absolute_path might be a symbol link pointing to the parent folder
        # of itself, which will cause infinite length of file paths.
        # Calling `absolute_path.exists()` to raise "OSError: Too many levels of symbol links"
        # to the user for this case.
        if not absolute_path.exists():
            raise FileNotFoundError("File not found: {}".format(absolute_path))

        if not relative_path_in_snapshot:
            raise ValueError("relative_path_in_snapshot must be specified.")
        self._relative_path = Path(relative_path_in_snapshot)

    @property
    def absolute_path(self):
        return self._absolute_path

    @property
    def relative_path(self):
        result = str(self._relative_path.as_posix())
        if self._absolute_path.is_dir():
            result += '/'
        return result

    def __repr__(self):
        return self.relative_path


class ComponentSnapshot:
    """Manage the snapshot of a component."""

    _DEFAULT_AMLIGNORE_FILE_CONFIG_KEY = 'component_amlignore_file'
    _LEGACY_AMLIGNORE_FILE_CONFIG_KEY = 'module_amlignore_file'

    def __init__(self, spec_file_path, additional_amlignore_file=None, logger=None):
        # Do the path resolve otherwise when the the spec_file_path is like 'component_spec.yaml'
        # which does not contain the parent paths, the `spec_file_path.parent` will be `.`
        # and result in the wrong folder structure of the created snapshot folder structure.
        self._spec_file_path = Path(spec_file_path).resolve()
        self._snapshot_folder = None

        if not additional_amlignore_file:
            additional_amlignore_file = _get_default_property(self._DEFAULT_AMLIGNORE_FILE_CONFIG_KEY)
            # fall back to look legacy aml ignore file.
            if additional_amlignore_file is None:
                additional_amlignore_file = _get_default_property(self._LEGACY_AMLIGNORE_FILE_CONFIG_KEY)
        self._additional_amlignore_file = \
            Path(additional_amlignore_file).resolve() if additional_amlignore_file else None

        if self._additional_amlignore_file:
            if not self._additional_amlignore_file.is_file():
                raise UserErrorException(
                    'The specified amlignore file: {0} does not exist.'.format(self._additional_amlignore_file))

        try:
            with open(spec_file_path, 'r') as f:
                self._spec_dict = ruamel.yaml.safe_load(f)
        except Exception as e:
            raise UserErrorException('Failed to load spec file {0}.\nException: \n{1}'.format(spec_file_path, e))

        if not logger:
            self.logger = logging.getLogger('snapshot')
        else:
            self.logger = logger

        self._check_additional_includes()

        # This will be set in component registration and only when yaml is local source
        self.entry_file_relative_path = None
        # The snapshot based on sweep component yaml
        self.sweep = None
        self._sweep_spec_relative_path = None

    @classmethod
    def from_spec(cls, spec_file_path, additional_amlignore_file=None, logger=None):
        """
        Create ComponentSnapshot instance from a component spec file, with special logic for sweep component.
        For other type components, this func has no difference with calling constructor directly.
        """

        result = cls(spec_file_path, additional_amlignore_file, logger)
        # If current spec file is a sweep component yaml
        if result.trial_file:
            sweep_snapshot = result
            result = ComponentSnapshot(spec_file_path=sweep_snapshot.trial_file, logger=logger)
            result.sweep = sweep_snapshot
        return result

    @property
    def base_path(self):
        """The base folder path of the snapshot."""
        # First, go to the folder that contains the spec file
        path = self._spec_file_path.parent

        # Then, if sourceDirectory specified in the component spec, apply as relative directory.
        if self.code:
            path = path / self.code
            if path.resolve() not in self._spec_file_path.parents:
                if self.is_vnext_yaml:
                    raise UserErrorException(
                        "Invalid code '{}': "
                        "Code snapshot must be the parent folders of the component yaml spec file. "
                        "Please refer to https://aka.ms/code-snapshot for details.".format(self.code)
                    )
                else:
                    raise UserErrorException(
                        "Invalid sourceDirectory '{}': "
                        "Source directory must be the parent folders of the module yaml spec file. "
                        "Please refer to https://aka.ms/module-source-directory for details.".format(
                            self.code)
                    )

        # Finally, resolve the path and return.
        return path.resolve()

    @property
    def code(self):
        if self.is_vnext_yaml:
            return get_value_by_key_path(
                dct=self._spec_dict,
                key_path='code'
            )
        else:
            return try_to_get_value_from_multiple_key_paths(
                dct=self._spec_dict,
                key_path_list=[
                    'implementation/container/sourceDirectory',
                    'implementation/parallel/sourceDirectory',
                    'implementation/hdinsight/sourceDirectory',
                ]
            )

    @property
    def spec_file_relative_path(self):
        return self._spec_file_path.relative_to(self.base_path.resolve())

    @property
    def conda_file_relative_path(self):
        if self.is_vnext_yaml:
            return try_to_get_value_from_multiple_key_paths(
                dct=self._spec_dict,
                key_path_list=[
                    'environment/conda/conda_dependencies_file',
                    'environment/conda/pip_requirements_file',
                ]
            )
        else:
            return try_to_get_value_from_multiple_key_paths(
                dct=self._spec_dict,
                key_path_list=[
                    'implementation/container/amlEnvironment/python/condaDependenciesFile',
                    'implementation/parallel/amlEnvironment/python/condaDependenciesFile',
                ]
            )

    @property
    def pip_file_relative_path(self):
        return try_to_get_value_from_multiple_key_paths(
            dct=self._spec_dict,
            key_path_list=[
                'implementation/container/amlEnvironment/python/pipRequirementsFile',
                'implementation/parallel/amlEnvironment/python/pipRequirementsFile',
            ]
        )

    @property
    def docker_file_relative_path(self):
        docker_file = None
        if self.is_vnext_yaml:
            docker_file = get_value_by_key_path(
                dct=self._spec_dict,
                key_path='environment/docker/build/dockerfile',
            )
            docker_file = docker_file[len(FILE_HINT_IN_YAML):] \
                if docker_file and docker_file.startswith(FILE_HINT_IN_YAML) else None
        return docker_file

    @property
    def trial_file_relative_path(self):
        """The trial yaml file relative path of sweep component."""
        trial = get_value_by_key_path(
            dct=self._spec_dict,
            key_path='trial'
        )
        if trial is None:
            return None
        # TODO: try startwith
        file_mark = trial.find(FILE_HINT_IN_YAML)
        return trial[((file_mark + 5) if file_mark > -1 else 0):].strip()

    @property
    def sweep_spec_relative_path(self):
        """The sweep yaml relative path in trial component snapshot."""
        if self._sweep_spec_relative_path:
            return self._sweep_spec_relative_path
        return self.sweep._spec_file_path.relative_to(self.base_path.resolve())

    @property
    def conda_file(self):
        """The conda file path of the component (if any)."""
        return self.get_file_or_raise(self.conda_file_relative_path, 'conda')

    @property
    def pip_file(self):
        return self.get_file_or_raise(self.pip_file_relative_path, 'pip requirement')

    @property
    def docker_file(self):
        """The docker file path of the component."""
        return self.get_file_or_raise(self.docker_file_relative_path, 'docker')

    @property
    def entry_file(self):
        # Need to ensure that entry_file_relative_path is initialized before this
        # Currently all code path can ensure that
        if self.entry_file_relative_path is not None and is_absolute(self.entry_file_relative_path):
            return None
        return self.get_file_or_raise(self.entry_file_relative_path, 'entry file')

    @property
    def trial_file(self):
        """The trial yaml file of sweep component."""
        return self.get_file_or_raise(self.trial_file_relative_path, 'trial')

    @property
    def additional_includes_file_path(self):
        """Additional includes file, should be base_path/spec_file_name.additional_includes."""
        additional_includes_file_name = self._spec_file_path.with_suffix('.additional_includes')
        return self.base_path / additional_includes_file_name

    @property
    def is_vnext_yaml(self):
        # Follow MT's logic, if $schema is defined, it's a new yaml
        schema = get_value_by_key_path(self._spec_dict, '$schema')
        return schema is not None

    def get_file_or_raise(self, relative_path, name):
        if relative_path:
            conda_file_path = self.base_path / relative_path
            if os.path.isfile(conda_file_path):
                return conda_file_path
            elif self.additional_includes:
                # handle case when file in additional includes
                for inc in self._iter_additional_includes():
                    if Path(inc.relative_path).resolve().as_posix() == Path(relative_path).resolve().as_posix():
                        return inc.absolute_path
            else:
                raise UserErrorException('Can not find {0} file: {1}.'.format(name, relative_path))

        return None

    def create_snapshot(self):
        return self._make_zipfile(snapshot_items_iterator=self._iter_files())

    def create_spec_snapshot(self):
        return self._make_zipfile(snapshot_items_iterator=self._get_spec_file_list())

    def _get_spec_file_list(self):
        yield SnapshotItem(self._spec_file_path, relative_path_in_snapshot=self.spec_file_relative_path)
        if self.conda_file:
            yield SnapshotItem(self.conda_file, relative_path_in_snapshot=self.conda_file_relative_path)
        if self.pip_file:
            yield SnapshotItem(self.pip_file, relative_path_in_snapshot=self.pip_file_relative_path)
        if self.docker_file:
            yield SnapshotItem(self.docker_file, relative_path_in_snapshot=self.docker_file_relative_path)
        if self.entry_file:
            yield SnapshotItem(self.entry_file, relative_path_in_snapshot=self.entry_file_relative_path)
        if self.sweep:
            yield from self._get_sweep_yaml_file()

    def _get_sweep_yaml_file(self):
        """Return the SnapshotItem of sweep yaml file."""
        if self.sweep._spec_file_path.as_posix().startswith(self.base_path.as_posix()):
            yield SnapshotItem(self.sweep._spec_file_path, relative_path_in_snapshot=self.sweep_spec_relative_path)
        else:
            # If sweep yaml is outside of the trial component folder
            # Dump a new sweep yaml file, and link it to the trial component folder root
            updated_spec_dict = {
                **self.sweep._spec_dict,
                'trial': "{}{}".format(FILE_HINT_IN_YAML, self.spec_file_relative_path.as_posix())
            }
            tmp_sweep_yaml_path = Path(tempfile.mkdtemp()) / self.sweep._spec_file_path.name
            with open(tmp_sweep_yaml_path, 'w') as fout:
                ruamel.yaml.safe_dump(updated_spec_dict, fout)
            # Set expected relative path
            self._sweep_spec_relative_path = Path(self.sweep._spec_file_path.name)
            yield SnapshotItem(tmp_sweep_yaml_path, relative_path_in_snapshot=self._sweep_spec_relative_path)

    def file_exists(self, relative_path):
        """Detect whether a given path exists in the snapshot."""
        if relative_path:
            # First, check snapshot folder
            if (self.base_path / relative_path).is_file():
                return True

            # If not found in snapshot folder, try to find in additional includes
            include_name = Path(relative_path).parts[0]
            for inc in self.additional_includes:
                if Path(inc).name == include_name:
                    full_path = (self.base_path / inc).parent / relative_path
                    if full_path.is_file():
                        return True

            # TODO: handle the case that the file is listed in ignore files.

        # Otherwise, not found
        return False

    @property
    def additional_amlignore_file(self):
        return self._additional_amlignore_file

    def _make_amlignore(self, snapshot_folder):
        if not self.additional_amlignore_file:
            return

        if not self._additional_amlignore_file.is_file():
            raise UserErrorException('The specified amlignore file: {0} is invalid.'
                                     .format(self._additional_amlignore_file))

        # Copy specified .amlignore to snapshot folder if there is not existing one in base folder
        merged_amlignore_file = snapshot_folder / '.amlignore'
        if not merged_amlignore_file.exists():
            self._copy_to(self.additional_amlignore_file, merged_amlignore_file)

        # Append content of specified .amlignore to ignore file in base folder if it exists
        elif merged_amlignore_file.is_file():
            with open(merged_amlignore_file, 'a') as fout, open(self.additional_amlignore_file, 'r') as fin:
                fout.write('\n\n# Additional ignore\n')
                for line in fin:
                    fout.write(line)
                self.logger.debug("Append content of {0} to {1}"
                                  .format(self.additional_amlignore_file, merged_amlignore_file))

        else:
            raise UserErrorException("Unrecognized amlignore file {}".format(merged_amlignore_file))

    @property
    def additional_includes(self):
        additional_includes = self._get_additional_includes_from_file()
        legacy_additional_includes = self._get_additional_includes_from_spec()

        if additional_includes is not None and legacy_additional_includes is not None:
            raise UserErrorException("The 'additionalIncludes' field in module spec is a duplicate configuration. "
                                     "Please remove it when a separate .additional_includes file is provided.")
        elif legacy_additional_includes is not None:
            self.logger.warning(
                "The 'additionalIncludes' in module spec is deprecated. "
                "Please set the additional includes in {} file, and save it to the same folder of {}. "
                "Refer to https://aka.ms/module-additional-includes for details.".format(
                    self._spec_file_path.with_suffix('.additional_includes').name,
                    self._spec_file_path.name
                )
            )
            additional_includes = legacy_additional_includes

        return additional_includes or []

    @property
    def hdinsight_pyfiles(self):
        """This property gets the pyFiles item inside HDInsight section."""
        # py files section has different location in module and component yamls, get them via different key path.
        if self.is_vnext_yaml:
            return self._get_hdi_pyfiles_for_key_path('hdinsight/py_files')
        else:
            return self._get_hdi_pyfiles_for_key_path('implementation/hdinsight/pyFiles')

    def _get_hdi_pyfiles_for_key_path(self, key_path):
        # get hdi pyfiles for different version of yamls according to key_path.
        pyfiles = get_value_by_key_path(dct=self._spec_dict, key_path=key_path)

        if not pyfiles:
            return None

        if isinstance(pyfiles, str):
            pyfiles = [pyfiles]

        # Note: this exception only prevents snapshot creation continuing, user won't see the error message.
        # That's because we call create_snapshot and validate async and check result of validate first, so user
        # only sees error message from validate.
        if not isinstance(pyfiles, list):
            raise UserErrorException(
                "The '{}' field in spec got an "
                "unexpected type, expected to be a list but got {}.'".format(key_path, type(pyfiles)))

        return pyfiles

    def _get_additional_includes_from_spec(self):
        additional_includes = try_to_get_value_from_multiple_key_paths(
            dct=self._spec_dict,
            key_path_list=[
                'implementation/container/additionalIncludes',
                'implementation/parallel/additionalIncludes',
                'implementation/hdinsight/additionalIncludes',
            ]
        )

        if not additional_includes:
            return None

        # Legacy additional includes is not supported in new yaml.
        if self.is_vnext_yaml:
            raise UserErrorException(
                "The 'additionalIncludes' field in component spec is not supported. "
                "Please set the additional includes in {} file, and save it to the same folder of {}. "
                "Refer to https://aka.ms/component-additional-includes for details.".format(
                    self._spec_file_path.with_suffix('.additional_includes').name,
                    self._spec_file_path.name
                )
            )

        if isinstance(additional_includes, str):
            additional_includes = [additional_includes]

        if not isinstance(additional_includes, list):
            raise UserErrorException("The 'additionalIncludes' field in spec got an unexpected type, "
                                     "expected to be a list but got {}.'".format(type(additional_includes)))

        return additional_includes

    def _get_additional_includes_from_file(self):
        additional_includes = None
        try:
            if self.additional_includes_file_path.is_file():
                with open(self.additional_includes_file_path) as f:
                    lines = f.readlines()
                    # Keep the additional_includes is None when the input is empty list
                    if lines:
                        additional_includes = [l.strip() for l in lines if len(l.strip()) > 0]
        except BaseException:
            self.logger.warning(
                "Failed to load additional_includes file: {0}.".format(self.additional_includes_file_path))
            self.logger.debug(
                "Failed to load additional_includes file: {0}.".format(self.additional_includes_file_path),
                exc_info=True)

        return additional_includes

    def _remove_suffix(self, path):
        """Given a path, remove the suffix from it.

        >>> str(Path('/mnt/c/hello.zip'))
        '/mnt/c/hello'
        """
        # Get the stem path name. i.e. For /mnt/c/hello.zip, find /mnt/c/hello
        return path.parent / path.stem

    def _should_be_treated_as_zipped_folder(self, path):
        """Given a path, detect whether it should be treated as a zipped folder.

        For example, given /mnt/c/hello.zip,
          1) If a file or folder named /mnt/c/hello.zip exists, return False
          2) Otherwise,
             a) If a folder named /mnt/c/hello, return True
             b) Otherwise, return False
        """
        if not path.suffix == '.zip':
            return False

        # The file or folder with the .zip suffix exists, not treated as zip folder
        if path.exists():
            return False

        # Get the stem path name. i.e. For /mnt/c/hello.zip, find /mnt/c/hello
        stem_path = self._remove_suffix(path)

        # If the folder /mnt/c/hello exists, return True, otherwise return False
        return stem_path.is_dir()

    def _check_additional_includes(self):
        for inc in self.additional_includes:
            self._check_additional_includes_item(inc, dst_folder=self.base_path)

    def _check_additional_includes_item(self, inc, dst_folder):
        inc_path = self.base_path / inc
        # If additional includes has not supported characters in it, resolve will fail.
        # In that case, throw a user error instead of a os error.
        try:
            src = inc_path.resolve()
        except OSError as e:
            raise UserErrorException('Failed to resolve additional includes: {}'.format(inc_path)) from e

        # If the resolved file name is different with the origin input file name,
        # it means that the origin input path wasn't specified to a file name
        # e.g. the path "../../" might be resolved to /foo/bar
        if inc_path.name != src.name:
            self.logger.warning("It's recommended to specify the folder or file name in a additional included path, "
                                "e.g. '../src', '../src/python/library1' and '../assets/LICENSE'. "
                                "The current value is: {0}".format(inc))

        if not src.exists() and not self._should_be_treated_as_zipped_folder(src):
            raise UserErrorException('additionalIncludes path {0} was not found.'.format(src))

        # Check if src is root directory
        if len(src.parents) == 0:
            raise UserErrorException('Root directory is not supported for additionalIncludes.')

        dst_path = dst_folder / src.name
        if dst_path.is_symlink():
            # If the dst_path is a symbolic link, check if it points to the same place of src.
            # If so, treat as a good case; Otherwise, raise error.
            if dst_path.resolve() != src.resolve():
                raise UserErrorException('Path {0} has already existed as a symbolic link to {1}. '
                                         'Please check additionalIncludes.'.format(dst_path, dst_path.resolve()))
        elif dst_path.exists():
            raise UserErrorException('Path {0} has already existed. Please check additionalIncludes.'.format(dst_path))

    def _symbol_link_exist(self):
        for f in self.base_path.glob('**/*'):
            if f.is_symlink():
                return True
        return False

    def _copy_to(self, src, dst, try_to_zip_folders=False, folder_to_lookup_ignore_file=None):
        """Copy src file to dst file or copy src file/directory to location under dst directory.

        :param: src: The file or folder to be copied.
        :param: dst: The target folder to be copied to.
        :param: try_to_zip_folders: When the `src` contains a `.zip` suffix, and the file does not exist,
                                    try to find the folder with same name and copy zipped file.
                                    For example, when src is '/mnt/c/hello.zip', but there is no 'hello.zip' file
                                    in /mnt/c, try to find whether there is a folder named '/mnt/c/hello/'.
                                    If exists, package the folder as 'hello.zip' and then copy to dst folder.
        :param: folder_to_lookup_ignore_file: Specify a folder to lookup ignore file.
                                              This is used only when `try_to_zip_folder` is True.
                                              When creating the zip file, the files listed in the ignore files
                                              are skipped.
        """
        src = src.resolve()
        if src.is_file():
            # Identical to copy() except that copy2() also attempts to preserve file metadata.
            _copy2(src, dst)
        elif src.is_dir():
            dst = dst / src.name
            copytree(src, dst)
        elif try_to_zip_folders and self._should_be_treated_as_zipped_folder(src):
            stem_path = self._remove_suffix(src)
            temp_zip_folder = Path(tempfile.mkdtemp()) / src.stem
            self._copy_to(stem_path, temp_zip_folder)
            zip_file = self._make_snapshot(temp_zip_folder, folder_to_lookup_ignore_file=folder_to_lookup_ignore_file)
            self._copy_to(Path(zip_file), dst)
        else:
            raise UserErrorException('Path {0} was not found.'.format(src))

    def _get_snapshot_folder(self) -> Path:
        if self._snapshot_folder:
            return self._snapshot_folder
        # always build snapshot in temp folder. Because in azure file share, reading files is time consuming,
        # but temp folders locates in the vm, reading from there is cheap.
        # Also, we used shutil.copy2 to preserve the modification date, which won't affect the cache logic.
        self._snapshot_folder = self._get_temp_snapshot_folder(snapshot_items_iterator=self._iter_files())
        return self._snapshot_folder

    def _make_snapshot(self, src_path, folder_to_lookup_ignore_file=None):
        """Make snapshot file and return its path given source file or directory."""
        src_path = Path(src_path)
        if not src_path.exists():
            raise FileNotFoundError("File or directory {} was not found.".format(src_path))
        if src_path.is_file() and src_path.suffix == '.zip':
            return str(src_path)

        temp_directory = Path(tempfile.mkdtemp())
        zip_file_path = str(temp_directory / (src_path.name + '.zip'))

        if not folder_to_lookup_ignore_file:
            folder_to_lookup_ignore_file = src_path
        if not Path(folder_to_lookup_ignore_file).is_dir():
            raise UserErrorException(
                "No such folder {} to lookup .amlignore from.".format(folder_to_lookup_ignore_file))

        exclude_function = get_project_ignore_file(str(folder_to_lookup_ignore_file)).is_file_excluded
        _make_zipfile(zip_file_path, str(src_path), exclude_function=exclude_function)
        return zip_file_path

    def _iter_additional_includes(self):
        # get ignore file in base folder
        ignore_files = []
        ignore_file = self._get_ignore_file_in_folder(str(self.base_path))
        if ignore_file:
            ignore_files.append(ignore_file)

        for inc in self.additional_includes:
            path = self.base_path / inc
            if self._should_be_treated_as_zipped_folder(path):
                folder_to_zip = self._remove_suffix(path)
                zip_file = self._make_zipfile(
                    snapshot_items_iterator=self._iter_files_in_folder(
                        folder_to_zip, ignore_files=ignore_files, iterating_additional_includes=True))
                yield SnapshotItem(absolute_path=zip_file, relative_path_in_snapshot=path.name)
            else:
                yield from self._iter_files_in_folder(
                    path, ignore_files=ignore_files, iterating_additional_includes=True)

    def _iter_files(self, skip_additional_includes=False):
        # Firstly, iterate files from main snapshot folder
        yield from self._iter_files_in_folder(
            self.base_path, include_top_level_folder=False, skip_additional_includes=skip_additional_includes)

        # Secondly, iterate files from each additional includes
        yield from self._iter_additional_includes()

        # Then, add sweep yaml file for sweep component
        if self.sweep:
            yield from self._get_sweep_yaml_file()

        # Then, create zip entry for implementation/hdinsight/pyFiles if needed
        # NOTE: If the pyFiles is specified as zipped, the unzipped version will also included in snapshot.
        # TODO: Exclude unzipped version from snapshot.
        if self.hdinsight_pyfiles:
            for entry in self.hdinsight_pyfiles:
                path = self.base_path / entry
                if self._should_be_treated_as_zipped_folder(path):
                    folder_to_zip = self._remove_suffix(path)
                    zip_file = self._make_zipfile(snapshot_items_iterator=self._iter_files_in_folder(folder_to_zip))
                    yield SnapshotItem(absolute_path=zip_file, relative_path_in_snapshot=path.name)
                else:
                    # TODO: check existance of each entry
                    pass

    def _is_ignored(self, path: Path, base_folder: Path, ignore_files: list, is_additional_includes=False):
        """Returns true if path is ignored in folder according to ignore files.

        :param path: The path to check.
        :param base_folder: Base folder of the project
        :param ignore_files: List of ignore files from base folder to current folder.
        :param is_additional_includes: If the path is additional included file.
        :return: bool
        """

        def _is_ignored_by_file(path, ignore_file_folder, ignore_file):
            if is_additional_includes and ignore_file_folder == self.base_path:
                # if ignore file is from base folder, additional includes relative path should start with base folder
                # and contain top level folder, eg: for additional includes libs/, relative path should be libs/xxx
                relative_path = self._get_relative_path_in_snapshot(path, base_folder, True).as_posix()
            else:
                # otherwise, just calculate relative path from current path to ignore file folder.
                relative_path = _relative_to(path, ignore_file_folder).as_posix()
            # use relative path and add / to dir so pattern like "folder/" works
            if path.is_dir():
                relative_path += '/'
            if ignore_file.is_file_excluded(relative_path):
                return True
            return False

        for ignore_file in ignore_files:
            ignore_file_folder = Path(ignore_file.get_path()).resolve().absolute().parent
            if _is_ignored_by_file(path, ignore_file_folder, ignore_file):
                return True

        # If not match with the normal ignore files,
        # check the additional amlignore file to see if there's any match.
        if self.additional_amlignore_file:
            # NOTE: Must use the relative path here since the additional amlignore file
            #       may not layout in the same tree of the source path.
            #       Absolute paths will cause the check fail for that case.
            if _is_ignored_by_file(path, base_folder, IgnoreFile(self.additional_amlignore_file)):
                return True

        # If the logic goes here, indicates that the file should not be ignored.
        return False

    def _folder_path_to_key_in_folder_cache(self, path: Path) -> str:
        """Change folder path to a key in folder -> content cache."""
        # Won't resolve the path since the path might be a symbolic link
        return path.as_posix()

    def iter_files_and_get_ignore_file_dict_in_parallel(self, path: Path) -> (dict, dict):
        """Iter files and store folder with ignore files to a dict.

        In remote file systems(eg: mounted ADLS), file related operations(eg: path.iterdir() file.exists()) runs slow.
        So we parallelize the path.iterdir, get_project_ignore_file and stored the results in memory to get a better
        performance.

        :param path: The folder to iterate.
        :return: A dict of folder -> contents and a dict of folders which contains ignore files
        """
        # step1: iterate and record all folders in parallel
        # use a shared object since we modify it in parallel
        manager = multiprocessing.Manager()
        all_folders = manager.dict()
        with TaskQueue(_parent_logger=self.logger) as task_queue:
            def iter_files_in_parallel(path: Path):
                contents = []
                for file in path.iterdir():
                    # store string instead of Path object to avoid obscure Windows path errors on multiprocessing
                    contents.append(file.absolute().as_posix())
                    if file.is_dir():
                        task_queue.add(iter_files_in_parallel, file)
                path_key = self._folder_path_to_key_in_folder_cache(path)
                all_folders[path_key] = contents

            iter_files_in_parallel(path)
            # Note: we added tasks that will dynamically add tasks to task queue, so we need to flush task queue until
            # it has no tasks left
            while not task_queue._tasks.empty():
                task_queue.flush(source='iter_files_in_parallel')

        # step2: get ignore file in each folder in parallel
        ignore_files = manager.dict()

        def get_ignore_file(path: str):
            ignore_file = get_project_ignore_file(path)
            if ignore_file.exists():
                ignore_files[path] = True

        with TaskQueue(_parent_logger=self.logger) as task_queue:
            for folder in all_folders.keys():
                task_queue.add(get_ignore_file, folder)
        return ignore_files, all_folders

    def _get_ignore_file_in_folder(self, folder: str) -> Optional[IgnoreFile]:
        """Return ignore file in folder if exists, otherwise return None."""
        ignore_file = get_project_ignore_file(folder)
        if ignore_file.exists():
            return ignore_file
        else:
            return None

    def _get_relative_path_in_snapshot(self, path: Path, folder: Path, is_additional_includes=False) -> Path:
        """Return relative path in snapshot.

        For normal snapshot item like base_folder/path/to/file, path/to/file will be returned.
        For additional include item like "../lib", relative path with folder name("lib") will be returned.
        """
        relative_path = path.relative_to(folder)
        if is_additional_includes:
            # folder must be resolved before getting name since it may be .. or ~ which do not have valid names
            folder_name = folder.resolve().name
            # Append folder_name to the top level of relative path if `include_top_level_folder` specified.
            relative_path = Path(folder_name) / relative_path
        return relative_path

    def _iter_files_in_folder(
            self,
            folder: Path,
            include_top_level_folder=True,
            skip_additional_includes=False,
            ignore_files: list = None,
            iterating_additional_includes=False
    ):
        """Iterate files in given folder.

        :param folder: The folder to iterate
        :param ignore_files: List of ignore files that should take affect when iterate. When iterating additional
        includes, the list contains ignore files in base folder. Otherwise, the list is empty.
        :param include_top_level_folder: For additional includes, we need to include top level folder in snapshot item.
        Say we have a additional include item "libs/", when we iterate it, we want to include the folder name "libs"
        in created snapshot item.
        :param skip_additional_includes: Skip iterate additional includes file. It's for component build, where
        additional includes file is resolved to actual contents.
        :param iterating_additional_includes: If is iterating additional includes.
        """
        if not ignore_files:
            ignore_files = []

        def create_snapshot_item(path):
            relative_path = self._get_relative_path_in_snapshot(path, folder, include_top_level_folder)
            return SnapshotItem(absolute_path=path, relative_path_in_snapshot=relative_path)

        def is_additional_includes(path: Path):
            return path == self.additional_includes_file_path

        def iter_files_recursively(
                path: Path, base_folder: Path, ignore_files: list, ignore_file_paths: dict, all_folders: dict):
            path_key = self._folder_path_to_key_in_folder_cache(path)
            # add ignore in current folder into list if exist
            ignore_file = None
            if path_key in ignore_file_paths.keys():
                ignore_file = self._get_ignore_file_in_folder(str(path))
            if ignore_file:
                ignore_files.append(ignore_file)

            # use folder contents in cache to avoid iterating files twice
            contents = all_folders[path_key]
            for file in contents:
                # file stored in contents is string, change back to Path object
                file = Path(file)
                if path == base_folder:
                    # only check skip additional includes file in base folder
                    if skip_additional_includes and is_additional_includes(file):
                        continue
                if self._is_ignored(file, base_folder, ignore_files, iterating_additional_includes):
                    self.logger.info('\tIgnored {}'.format(file.resolve().absolute()))
                    continue
                yield create_snapshot_item(file)
                if file.is_dir():
                    yield from iter_files_recursively(file, base_folder, ignore_files, ignore_file_paths, all_folders)

            if ignore_file:
                ignore_files.pop()

        if Path(folder).is_file():
            # Yield the item directly if it is a file
            yield SnapshotItem(absolute_path=folder, relative_path_in_snapshot=folder.name)
        else:
            # Otherwise treat as a folder
            # We need absolute path because in memory cache use the folder path as key, call resolve twice to resolve
            # windows short path to normal path.
            folder = folder.resolve().absolute().resolve()
            if include_top_level_folder:
                yield create_snapshot_item(folder)
            # collect all possible ignore files in advance in parallel to improve perf
            ignore_file_paths, all_folders = self.iter_files_and_get_ignore_file_dict_in_parallel(folder)
            yield from iter_files_recursively(folder, folder, ignore_files, ignore_file_paths, all_folders)

    def _make_zipfile(self, snapshot_items_iterator, zip_file_name='temp.zip'):
        temp_directory = Path(tempfile.mkdtemp())
        zip_file = temp_directory / zip_file_name
        with zipfile.ZipFile(zip_file, 'w') as zf:
            for snapshot_item in snapshot_items_iterator:
                zf.write(snapshot_item.absolute_path, snapshot_item.relative_path)
            return zip_file

    def _create_snapshot_in_folder(self, folder, snapshot_items_iterator) -> Path:
        self.logger.info('Start collecting files in snapshot...')
        # file count
        file_count = 0
        # snapshot size
        self.total_size = 0
        with TimerContext() as timer_context:
            # Here we copy files in parallel to have a better performance. Note when file number is small and
            # file size is big(eg: 2 1GB files): copy in parallel may have perf regression. Since the case is hard to
            # reproduce in real world, we will keep current implementation.
            with TaskQueue(flush_timeout_seconds=AZUREML_SNAPSHOT_DEFAULT_TIMEOUT,
                           _ident="snapshot_copy_files", _parent_logger=self.logger) as task_queue:
                for snapshot_item in snapshot_items_iterator:
                    if snapshot_item.absolute_path.is_file():
                        dst = os.path.join(folder, snapshot_item.relative_path)
                        if os.path.exists(dst):
                            self.logger.info('\tOverwrite {}'.format(snapshot_item.absolute_path))
                        else:
                            self.logger.info('\tCollected {}'.format(snapshot_item.absolute_path))
                        # copy files in parallel
                        task_queue.add(_copy2, snapshot_item.absolute_path, dst)
                        self.total_size += os.path.getsize(snapshot_item.absolute_path)
                        file_count += 1
                    else:
                        target_dir = os.path.join(folder, snapshot_item.relative_path)
                        if os.path.exists(target_dir):
                            self.logger.info('\tSkipped {}'.format(snapshot_item.absolute_path))
                        else:
                            os.mkdir(target_dir)
            duration_seconds = timer_context.get_duration_seconds()
            self.logger.info('Collected {} files in {:.2f} seconds, total size {:.2f} KB'.format(
                file_count, duration_seconds, self.total_size / 1024))
            track_dimensions = {
                'collected_file_count': file_count,
                'collected_file_size': self.total_size / 1024,
                'collect_duration_seconds': duration_seconds
            }
            _LoggerFactory.add_track_dimensions(self.logger, track_dimensions)
        return Path(folder)

    def _get_temp_snapshot_folder(self, snapshot_items_iterator) -> Path:
        temp_directory = Path(tempfile.mkdtemp())
        return self._create_snapshot_in_folder(temp_directory, snapshot_items_iterator)


class LocalComponentSnapshot(ComponentSnapshot):
    """A local version of a component snapshot.

    The snapshot only supports vnext yaml(eg: inline additional includes is not supported).
    """

    def __init__(self, spec_file_path, additional_amlignore_file=None, snapshot_folder=None, logger=None):
        if _looks_like_a_url(spec_file_path):
            raise UserErrorException(
                'Only local file is supported when building a local snapshot, got {}'.format(spec_file_path))
        path = check_spec_file(spec_file_path)
        super(LocalComponentSnapshot, self).__init__(path, additional_amlignore_file, logger)
        if snapshot_folder is not None:
            # If user specified snapshot folder, use it
            if os.path.exists(snapshot_folder) and os.path.samefile(snapshot_folder, self.base_path):
                raise UserErrorException(
                    'Output directory {} is the same as project folder, which is not allowed.'.format(snapshot_folder))
            self._snapshot_build_folder = snapshot_folder
        else:
            # By default, the build folder will be COMPONENT_SNAPSHOT_DIR_NAME inside base path
            self._snapshot_build_folder = self.base_path / COMPONENT_SNAPSHOT_DIR_NAME
        # Clean up snapshot directory if not empty
        try:
            create_or_cleanup_folder(self._snapshot_build_folder)
        except Exception as e:
            raise RuntimeError('Failed to create or clean up snapshot folder: {}. Reason: {}'.format(
                snapshot_folder, e))

    def _get_additional_includes_from_spec(self):
        """Inline additional includes is not supported because it doesn't exist in vnext yaml."""
        additional_includes = try_to_get_value_from_multiple_key_paths(
            dct=self._spec_dict,
            key_path_list=[
                'implementation/container/additionalIncludes',
                'implementation/parallel/additionalIncludes',
                'implementation/hdinsight/additionalIncludes',
            ]
        )

        if additional_includes:
            raise UserErrorException(
                'Inline additional includes found: {}, which is not supported.'.format(additional_includes))
        else:
            return None

    def _create_snapshot_in_folder(self, folder, snapshot_items_iterator) -> Path:
        """Create snapshot with detailed log"""
        folder = Path(folder)
        from azure.ml.component.dsl._pipeline_project import PipelineProject
        self.logger.info(PipelineProject.version_hint())
        self.logger.info('========== Build started: {} =========='.format(folder.as_posix()))
        self.logger.info('\n')

        super(LocalComponentSnapshot, self)._create_snapshot_in_folder(folder, snapshot_items_iterator)

        self.logger.info('\n')
        self.logger.info('Successfully built snapshot in {}'.format(folder.as_posix()))
        return folder

    def _get_snapshot_folder(self):
        """Create snapshot in snapshot folder, returns created snapshot folder."""
        if self._snapshot_folder:
            return self._snapshot_folder

        # set skip_additional_includes to True so the snapshot folder does not contain additional includes file
        self._snapshot_folder = self._create_snapshot_in_folder(
            self._snapshot_build_folder, self._iter_files(skip_additional_includes=True))
        return self._snapshot_folder

    def _is_ignored(self, path: Path, base_folder: Path, ignore_files: list, is_additional_includes=False):
        """Returns true if path is ignored in folder according to ignore files.

        Note: Snapshot build folder files will be ignored implicitly

        :param path: The path to check.
        :param base_folder: Base folder of the project
        :param ignore_files: List of ignore files from base folder to current folder.
        :param is_additional_includes: If the path is additional included file.
        :return: bool
        """
        if _relative_to(path, self._snapshot_build_folder) is not None:
            return True
        return super(LocalComponentSnapshot, self)._is_ignored(
            path, base_folder, ignore_files, is_additional_includes)
