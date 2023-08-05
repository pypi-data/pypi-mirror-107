# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DatastoreSetting(Model):
    """DatastoreSetting.

    :param data_store_name:
    :type data_store_name: str
    """

    _attribute_map = {
        'data_store_name': {'key': 'dataStoreName', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(DatastoreSetting, self).__init__(**kwargs)
        self.data_store_name = kwargs.get('data_store_name', None)
