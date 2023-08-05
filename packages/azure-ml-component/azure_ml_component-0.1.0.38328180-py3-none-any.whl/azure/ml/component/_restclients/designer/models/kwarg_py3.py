# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class Kwarg(Model):
    """Kwarg.

    :param key:
    :type key: str
    :param value:
    :type value: str
    """

    _attribute_map = {
        'key': {'key': 'key', 'type': 'str'},
        'value': {'key': 'value', 'type': 'str'},
    }

    def __init__(self, *, key: str=None, value: str=None, **kwargs) -> None:
        super(Kwarg, self).__init__(**kwargs)
        self.key = key
        self.value = value
