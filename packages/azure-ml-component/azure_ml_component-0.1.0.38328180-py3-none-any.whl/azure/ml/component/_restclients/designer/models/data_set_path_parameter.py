# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DataSetPathParameter(Model):
    """DataSetPathParameter.

    :param name:
    :type name: str
    :param documentation:
    :type documentation: str
    :param default_value:
    :type default_value: ~designer.models.DataSetDefinitionValue
    :param is_optional:
    :type is_optional: bool
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'documentation': {'key': 'documentation', 'type': 'str'},
        'default_value': {'key': 'defaultValue', 'type': 'DataSetDefinitionValue'},
        'is_optional': {'key': 'isOptional', 'type': 'bool'},
    }

    def __init__(self, **kwargs):
        super(DataSetPathParameter, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.documentation = kwargs.get('documentation', None)
        self.default_value = kwargs.get('default_value', None)
        self.is_optional = kwargs.get('is_optional', None)
