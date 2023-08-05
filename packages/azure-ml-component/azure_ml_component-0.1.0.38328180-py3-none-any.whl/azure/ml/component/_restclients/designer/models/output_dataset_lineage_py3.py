# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class OutputDatasetLineage(Model):
    """OutputDatasetLineage.

    :param identifier:
    :type identifier: ~designer.models.DatasetIdentifier
    :param output_type: Possible values include: 'RunOutput', 'Reference'
    :type output_type: str or ~designer.models.DatasetOutputType
    :param output_details:
    :type output_details: ~designer.models.DatasetOutputDetails
    """

    _attribute_map = {
        'identifier': {'key': 'identifier', 'type': 'DatasetIdentifier'},
        'output_type': {'key': 'outputType', 'type': 'str'},
        'output_details': {'key': 'outputDetails', 'type': 'DatasetOutputDetails'},
    }

    def __init__(self, *, identifier=None, output_type=None, output_details=None, **kwargs) -> None:
        super(OutputDatasetLineage, self).__init__(**kwargs)
        self.identifier = identifier
        self.output_type = output_type
        self.output_details = output_details
