# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class GraphLayoutCreationInfo(Model):
    """GraphLayoutCreationInfo.

    :param node_layouts: This is a dictionary
    :type node_layouts: dict[str, ~designer.models.NodeLayout]
    """

    _attribute_map = {
        'node_layouts': {'key': 'nodeLayouts', 'type': '{NodeLayout}'},
    }

    def __init__(self, **kwargs):
        super(GraphLayoutCreationInfo, self).__init__(**kwargs)
        self.node_layouts = kwargs.get('node_layouts', None)
