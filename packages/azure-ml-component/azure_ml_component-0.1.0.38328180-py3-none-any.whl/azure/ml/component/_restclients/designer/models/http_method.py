# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class HttpMethod(Model):
    """HttpMethod.

    :param method:
    :type method: str
    """

    _attribute_map = {
        'method': {'key': 'method', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(HttpMethod, self).__init__(**kwargs)
        self.method = kwargs.get('method', None)
