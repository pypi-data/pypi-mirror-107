# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PortInfo(Model):
    """PortInfo.

    :param node_id:
    :type node_id: str
    :param port_name:
    :type port_name: str
    :param graph_port_name:
    :type graph_port_name: str
    :param web_service_port:
    :type web_service_port: str
    """

    _attribute_map = {
        'node_id': {'key': 'nodeId', 'type': 'str'},
        'port_name': {'key': 'portName', 'type': 'str'},
        'graph_port_name': {'key': 'graphPortName', 'type': 'str'},
        'web_service_port': {'key': 'webServicePort', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(PortInfo, self).__init__(**kwargs)
        self.node_id = kwargs.get('node_id', None)
        self.port_name = kwargs.get('port_name', None)
        self.graph_port_name = kwargs.get('graph_port_name', None)
        self.web_service_port = kwargs.get('web_service_port', None)
