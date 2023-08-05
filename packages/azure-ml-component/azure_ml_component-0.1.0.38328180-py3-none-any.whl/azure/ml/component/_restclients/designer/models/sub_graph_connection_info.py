# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SubGraphConnectionInfo(Model):
    """SubGraphConnectionInfo.

    :param node_id:
    :type node_id: str
    :param port_name:
    :type port_name: str
    """

    _attribute_map = {
        'node_id': {'key': 'nodeId', 'type': 'str'},
        'port_name': {'key': 'portName', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(SubGraphConnectionInfo, self).__init__(**kwargs)
        self.node_id = kwargs.get('node_id', None)
        self.port_name = kwargs.get('port_name', None)
