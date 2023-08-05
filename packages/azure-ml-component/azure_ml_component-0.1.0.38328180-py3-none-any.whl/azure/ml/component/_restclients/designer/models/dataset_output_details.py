# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DatasetOutputDetails(Model):
    """DatasetOutputDetails.

    :param output_name:
    :type output_name: str
    """

    _attribute_map = {
        'output_name': {'key': 'outputName', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(DatasetOutputDetails, self).__init__(**kwargs)
        self.output_name = kwargs.get('output_name', None)
