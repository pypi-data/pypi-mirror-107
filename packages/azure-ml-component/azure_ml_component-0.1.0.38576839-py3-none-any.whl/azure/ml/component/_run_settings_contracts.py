# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Support more contracts in runsettings. Currently, we support [BanditPolicy, MedianStoppingPolicy,
TruncationSelectionPolicy, NoTerminationPolicy] from azureml.train.hyperdrive for sweep.early_termination.
Soon will support new classes [Environment, Docker, Conda] for environment override."""

from ._environment import Docker, Conda


_docker_image_yaml_template = """
docker:
  image: {}
"""


_docker_build_file_yaml_template = """
docker:
  build:
    dockerfile: |-
{}
"""


def _docker_converter(obj: Docker):
    if obj.image:
        return _docker_image_yaml_template.format(obj.image).strip()
    elif obj.file:
        with open(obj.file) as fin:
            lines = fin.read().splitlines()
            lines_str = ['      {}'.format(l) for l in lines]
            return _docker_build_file_yaml_template.format('\n'.join(lines_str)).strip()
    return None


_conda_pip_requirement_file_yaml_template = """
conda:
  conda_dependencies:
    name: project_environment
    dependencies:
{}
"""


_conda_conda_file_yaml_template = """
conda:
  conda_dependencies:
{}
"""


def _conda_converter(obj: Conda):
    if obj.pip_requirement_file:
        with open(obj.pip_requirement_file) as fin:
            packs = fin.read().splitlines()
            packs_str = ['    - {}'.format(p) for p in packs]
            return _conda_pip_requirement_file_yaml_template.format('\n'.join(packs_str)).strip()
    elif obj.conda_file:
        with open(obj.conda_file) as fin:
            lines = fin.read().splitlines()
            lines_str = ['    {}'.format(l) for l in lines]
            return _conda_conda_file_yaml_template.format('\n'.join(lines_str)).strip()
    return None


def _bandit_policy_converter(obj):
    result = {
        'policy_type': 'bandit',
        'evaluation_interval': obj._evaluation_interval,
        'delay_evaluation': obj._delay_evaluation
    }
    if obj._slack_factor:
        result['slack_factor'] = obj._slack_factor
    else:
        result['slack_amount'] = obj._properties.get('slack_amount')
    return result


def _median_stopping_policy_converter(obj):
    return {
        'policy_type': 'median_stopping',
        'evaluation_interval': obj._evaluation_interval,
        'delay_evaluation': obj._delay_evaluation
    }


def _truncation_selection_policy_converter(obj):
    return {
        'policy_type': 'truncation_selection',
        'truncation_percentage': obj._truncation_percentage,
        'evaluation_interval': obj._evaluation_interval,
        'delay_evaluation': obj._delay_evaluation
    }


def _no_termination_policy_converter(obj):
    return {
        'policy_type': 'default'
    }


# For new classes support, we just add more converters here
def _get_converters_by_section_name(section_name):
    if section_name == 'early_termination':
        # This part is used for supporting sweep_component.runsettings.sweep.early_termination = Policy
        try:
            from azureml.train.hyperdrive import BanditPolicy, MedianStoppingPolicy, TruncationSelectionPolicy, \
                NoTerminationPolicy
            return {
                BanditPolicy: _bandit_policy_converter,
                MedianStoppingPolicy: _median_stopping_policy_converter,
                TruncationSelectionPolicy: _truncation_selection_policy_converter,
                NoTerminationPolicy: _no_termination_policy_converter,
            }
        except Exception:
            return {}
    return {}


def try_convert_obj_to_dict(section_name, obj):
    """Return dict if obj is dict or there is a dict-converter for obj, otherwise return None."""
    obj_type = type(obj)
    if obj_type == dict:
        return obj
    converters = _get_converters_by_section_name(section_name)
    if obj_type in converters:
        converter = converters[obj_type]
        # In case the converter throws exception
        try:
            return converter(obj)
        except Exception as e:
            raise Exception("Failed to set '{}' from type '{}'.".format(section_name, obj_type)) from e
    return None


_parameter_converters = {
    'environment.docker': {
        Docker: _docker_converter
    },
    'environment.conda': {
        Conda: _conda_converter
    }
}


def try_convert_obj_to_value(parameter_id, obj, expected_type):
    obj_type = type(obj)
    if obj_type == expected_type:
        return obj
    # Look up for a converter
    if parameter_id in _parameter_converters:
        if obj_type in _parameter_converters[parameter_id]:
            converter = _parameter_converters[parameter_id][obj_type]
            try:
                return converter(obj)
            except Exception as e:
                raise Exception("Failed to set '{}' from type '{}'.".format(parameter_id, obj_type)) from e
    # Otherwise, return obj directly
    return obj
