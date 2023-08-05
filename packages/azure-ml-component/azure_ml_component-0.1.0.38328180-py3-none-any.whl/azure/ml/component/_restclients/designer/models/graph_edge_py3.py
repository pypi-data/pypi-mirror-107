# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GraphEdge(Model):
    """GraphEdge.

    :param source_output_port:
    :type source_output_port: ~designer.models.PortInfo
    :param destination_input_port:
    :type destination_input_port: ~designer.models.PortInfo
    """

    _attribute_map = {
        'source_output_port': {'key': 'sourceOutputPort', 'type': 'PortInfo'},
        'destination_input_port': {'key': 'destinationInputPort', 'type': 'PortInfo'},
    }

    def __init__(self, *, source_output_port=None, destination_input_port=None, **kwargs) -> None:
        super(GraphEdge, self).__init__(**kwargs)
        self.source_output_port = source_output_port
        self.destination_input_port = destination_input_port
