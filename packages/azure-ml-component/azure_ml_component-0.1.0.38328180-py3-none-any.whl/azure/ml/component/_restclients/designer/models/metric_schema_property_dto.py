# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MetricSchemaPropertyDto(Model):
    """MetricSchemaPropertyDto.

    :param property_id:
    :type property_id: str
    :param name:
    :type name: str
    :param type:
    :type type: str
    """

    _attribute_map = {
        'property_id': {'key': 'propertyId', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(MetricSchemaPropertyDto, self).__init__(**kwargs)
        self.property_id = kwargs.get('property_id', None)
        self.name = kwargs.get('name', None)
        self.type = kwargs.get('type', None)
