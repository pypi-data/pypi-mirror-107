# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ControlInput(Model):
    """ControlInput.

    :param name:
    :type name: str
    :param default_value: Possible values include: 'False', 'True'
    :type default_value: str or ~designer.models.ControlInputValue
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'default_value': {'key': 'defaultValue', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(ControlInput, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.default_value = kwargs.get('default_value', None)
