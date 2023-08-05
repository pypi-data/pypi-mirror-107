# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class StructuredInterfaceInput(Model):
    """StructuredInterfaceInput.

    :param name:
    :type name: str
    :param label:
    :type label: str
    :param data_type_ids_list:
    :type data_type_ids_list: list[str]
    :param is_optional:
    :type is_optional: bool
    :param description:
    :type description: str
    :param skip_processing:
    :type skip_processing: bool
    :param is_resource:
    :type is_resource: bool
    :param data_store_mode: Possible values include: 'None', 'Mount',
     'Download', 'Upload', 'Direct', 'Hdfs', 'Link'
    :type data_store_mode: str or ~designer.models.DataStoreMode
    :param path_on_compute:
    :type path_on_compute: str
    :param overwrite:
    :type overwrite: bool
    :param data_reference_name:
    :type data_reference_name: str
    :param dataset_types:
    :type dataset_types: list[str or ~designer.models.DatasetType]
    """

    _validation = {
        'dataset_types': {'unique': True},
    }

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'label': {'key': 'label', 'type': 'str'},
        'data_type_ids_list': {'key': 'dataTypeIdsList', 'type': '[str]'},
        'is_optional': {'key': 'isOptional', 'type': 'bool'},
        'description': {'key': 'description', 'type': 'str'},
        'skip_processing': {'key': 'skipProcessing', 'type': 'bool'},
        'is_resource': {'key': 'isResource', 'type': 'bool'},
        'data_store_mode': {'key': 'dataStoreMode', 'type': 'str'},
        'path_on_compute': {'key': 'pathOnCompute', 'type': 'str'},
        'overwrite': {'key': 'overwrite', 'type': 'bool'},
        'data_reference_name': {'key': 'dataReferenceName', 'type': 'str'},
        'dataset_types': {'key': 'datasetTypes', 'type': '[str]'},
    }

    def __init__(self, **kwargs):
        super(StructuredInterfaceInput, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.label = kwargs.get('label', None)
        self.data_type_ids_list = kwargs.get('data_type_ids_list', None)
        self.is_optional = kwargs.get('is_optional', None)
        self.description = kwargs.get('description', None)
        self.skip_processing = kwargs.get('skip_processing', None)
        self.is_resource = kwargs.get('is_resource', None)
        self.data_store_mode = kwargs.get('data_store_mode', None)
        self.path_on_compute = kwargs.get('path_on_compute', None)
        self.overwrite = kwargs.get('overwrite', None)
        self.data_reference_name = kwargs.get('data_reference_name', None)
        self.dataset_types = kwargs.get('dataset_types', None)
