# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ModuleDtoWithValidateStatus(Model):
    """ModuleDtoWithValidateStatus.

    :param existing_module_entity:
    :type existing_module_entity: ~designer.models.ModuleEntity
    :param status: Possible values include: 'NewModule', 'NewVersion',
     'Conflict', 'ParseError', 'ProcessRequestError'
    :type status: str or ~designer.models.ModuleInfoFromYamlStatusEnum
    :param status_details:
    :type status_details: str
    :param namespace:
    :type namespace: str
    :param tags:
    :type tags: list[str]
    :param display_name:
    :type display_name: str
    :param dict_tags:
    :type dict_tags: dict[str, str]
    :param module_name:
    :type module_name: str
    :param entity_status: Possible values include: 'Active', 'Deprecated',
     'Disabled'
    :type entity_status: str or ~designer.models.EntityStatus
    :param created_date:
    :type created_date: datetime
    :param last_modified_date:
    :type last_modified_date: datetime
    :param versions:
    :type versions: list[~designer.models.AzureMLModuleVersionDescriptor]
    :param default_version:
    :type default_version: str
    :param module_scope: Possible values include: 'All', 'Global',
     'Workspace', 'Anonymous', 'Step', 'Draft'
    :type module_scope: str or ~designer.models.ModuleScope
    :param module_version_id:
    :type module_version_id: str
    :param description:
    :type description: str
    :param owner:
    :type owner: str
    :param job_type:
    :type job_type: str
    :param yaml_link:
    :type yaml_link: str
    :param yaml_link_with_commit_sha:
    :type yaml_link_with_commit_sha: str
    :param family_id:
    :type family_id: str
    :param help_document:
    :type help_document: str
    :param codegen_by:
    :type codegen_by: str
    :param entry:
    :type entry: str
    :param os_type:
    :type os_type: str
    :param module_source_type: Possible values include: 'Unknown', 'Local',
     'GithubFile', 'GithubFolder', 'DevopsArtifactsZip'
    :type module_source_type: str or ~designer.models.ModuleSourceType
    :param registered_by:
    :type registered_by: str
    :param module_version:
    :type module_version: str
    :param is_default_module_version:
    :type is_default_module_version: bool
    :param module_entity:
    :type module_entity: ~designer.models.ModuleEntity
    :param input_types:
    :type input_types: list[str]
    :param output_types:
    :type output_types: list[str]
    :param run_setting_parameters:
    :type run_setting_parameters: list[~designer.models.RunSettingParameter]
    :param require_gpu:
    :type require_gpu: bool
    :param module_python_interface:
    :type module_python_interface: ~designer.models.ModulePythonInterface
    :param snapshot_id:
    :type snapshot_id: str
    :param yaml_str:
    :type yaml_str: str
    """

    _attribute_map = {
        'existing_module_entity': {'key': 'existingModuleEntity', 'type': 'ModuleEntity'},
        'status': {'key': 'status', 'type': 'str'},
        'status_details': {'key': 'statusDetails', 'type': 'str'},
        'namespace': {'key': 'namespace', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '[str]'},
        'display_name': {'key': 'displayName', 'type': 'str'},
        'dict_tags': {'key': 'dictTags', 'type': '{str}'},
        'module_name': {'key': 'moduleName', 'type': 'str'},
        'entity_status': {'key': 'entityStatus', 'type': 'str'},
        'created_date': {'key': 'createdDate', 'type': 'iso-8601'},
        'last_modified_date': {'key': 'lastModifiedDate', 'type': 'iso-8601'},
        'versions': {'key': 'versions', 'type': '[AzureMLModuleVersionDescriptor]'},
        'default_version': {'key': 'defaultVersion', 'type': 'str'},
        'module_scope': {'key': 'moduleScope', 'type': 'str'},
        'module_version_id': {'key': 'moduleVersionId', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'owner': {'key': 'owner', 'type': 'str'},
        'job_type': {'key': 'jobType', 'type': 'str'},
        'yaml_link': {'key': 'yamlLink', 'type': 'str'},
        'yaml_link_with_commit_sha': {'key': 'yamlLinkWithCommitSha', 'type': 'str'},
        'family_id': {'key': 'familyId', 'type': 'str'},
        'help_document': {'key': 'helpDocument', 'type': 'str'},
        'codegen_by': {'key': 'codegenBy', 'type': 'str'},
        'entry': {'key': 'entry', 'type': 'str'},
        'os_type': {'key': 'osType', 'type': 'str'},
        'module_source_type': {'key': 'moduleSourceType', 'type': 'str'},
        'registered_by': {'key': 'registeredBy', 'type': 'str'},
        'module_version': {'key': 'moduleVersion', 'type': 'str'},
        'is_default_module_version': {'key': 'isDefaultModuleVersion', 'type': 'bool'},
        'module_entity': {'key': 'moduleEntity', 'type': 'ModuleEntity'},
        'input_types': {'key': 'inputTypes', 'type': '[str]'},
        'output_types': {'key': 'outputTypes', 'type': '[str]'},
        'run_setting_parameters': {'key': 'runSettingParameters', 'type': '[RunSettingParameter]'},
        'require_gpu': {'key': 'requireGpu', 'type': 'bool'},
        'module_python_interface': {'key': 'modulePythonInterface', 'type': 'ModulePythonInterface'},
        'snapshot_id': {'key': 'snapshotId', 'type': 'str'},
        'yaml_str': {'key': 'yamlStr', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(ModuleDtoWithValidateStatus, self).__init__(**kwargs)
        self.existing_module_entity = kwargs.get('existing_module_entity', None)
        self.status = kwargs.get('status', None)
        self.status_details = kwargs.get('status_details', None)
        self.namespace = kwargs.get('namespace', None)
        self.tags = kwargs.get('tags', None)
        self.display_name = kwargs.get('display_name', None)
        self.dict_tags = kwargs.get('dict_tags', None)
        self.module_name = kwargs.get('module_name', None)
        self.entity_status = kwargs.get('entity_status', None)
        self.created_date = kwargs.get('created_date', None)
        self.last_modified_date = kwargs.get('last_modified_date', None)
        self.versions = kwargs.get('versions', None)
        self.default_version = kwargs.get('default_version', None)
        self.module_scope = kwargs.get('module_scope', None)
        self.module_version_id = kwargs.get('module_version_id', None)
        self.description = kwargs.get('description', None)
        self.owner = kwargs.get('owner', None)
        self.job_type = kwargs.get('job_type', None)
        self.yaml_link = kwargs.get('yaml_link', None)
        self.yaml_link_with_commit_sha = kwargs.get('yaml_link_with_commit_sha', None)
        self.family_id = kwargs.get('family_id', None)
        self.help_document = kwargs.get('help_document', None)
        self.codegen_by = kwargs.get('codegen_by', None)
        self.entry = kwargs.get('entry', None)
        self.os_type = kwargs.get('os_type', None)
        self.module_source_type = kwargs.get('module_source_type', None)
        self.registered_by = kwargs.get('registered_by', None)
        self.module_version = kwargs.get('module_version', None)
        self.is_default_module_version = kwargs.get('is_default_module_version', None)
        self.module_entity = kwargs.get('module_entity', None)
        self.input_types = kwargs.get('input_types', None)
        self.output_types = kwargs.get('output_types', None)
        self.run_setting_parameters = kwargs.get('run_setting_parameters', None)
        self.require_gpu = kwargs.get('require_gpu', None)
        self.module_python_interface = kwargs.get('module_python_interface', None)
        self.snapshot_id = kwargs.get('snapshot_id', None)
        self.yaml_str = kwargs.get('yaml_str', None)
