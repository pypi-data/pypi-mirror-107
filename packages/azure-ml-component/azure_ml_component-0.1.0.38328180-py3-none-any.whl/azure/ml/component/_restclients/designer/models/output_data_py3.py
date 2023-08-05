# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class OutputData(Model):
    """OutputData.

    :param output_location:
    :type output_location: ~designer.models.ExecutionDataLocation
    :param mechanism: Possible values include: 'Upload', 'Mount', 'Hdfs',
     'Link'
    :type mechanism: str or ~designer.models.OutputMechanism
    :param additional_options:
    :type additional_options: ~designer.models.OutputOptions
    """

    _attribute_map = {
        'output_location': {'key': 'outputLocation', 'type': 'ExecutionDataLocation'},
        'mechanism': {'key': 'mechanism', 'type': 'str'},
        'additional_options': {'key': 'additionalOptions', 'type': 'OutputOptions'},
    }

    def __init__(self, *, output_location=None, mechanism=None, additional_options=None, **kwargs) -> None:
        super(OutputData, self).__init__(**kwargs)
        self.output_location = output_location
        self.mechanism = mechanism
        self.additional_options = additional_options
