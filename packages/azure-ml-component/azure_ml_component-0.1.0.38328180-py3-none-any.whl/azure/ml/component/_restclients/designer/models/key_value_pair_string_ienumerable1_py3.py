# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class KeyValuePairStringIEnumerable1(Model):
    """KeyValuePairStringIEnumerable1.

    :param key:
    :type key: str
    :param value:
    :type value: list[str]
    """

    _attribute_map = {
        'key': {'key': 'key', 'type': 'str'},
        'value': {'key': 'value', 'type': '[str]'},
    }

    def __init__(self, *, key: str=None, value=None, **kwargs) -> None:
        super(KeyValuePairStringIEnumerable1, self).__init__(**kwargs)
        self.key = key
        self.value = value
