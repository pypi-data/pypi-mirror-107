# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PipelineRunStatus(Model):
    """PipelineRunStatus.

    :param status_code: Possible values include: 'NotStarted', 'Running',
     'Failed', 'Finished', 'Canceled'
    :type status_code: str or ~designer.models.PipelineRunStatusCode
    :param status_detail:
    :type status_detail: str
    :param creation_time:
    :type creation_time: datetime
    :param end_time:
    :type end_time: datetime
    """

    _attribute_map = {
        'status_code': {'key': 'statusCode', 'type': 'str'},
        'status_detail': {'key': 'statusDetail', 'type': 'str'},
        'creation_time': {'key': 'creationTime', 'type': 'iso-8601'},
        'end_time': {'key': 'endTime', 'type': 'iso-8601'},
    }

    def __init__(self, **kwargs):
        super(PipelineRunStatus, self).__init__(**kwargs)
        self.status_code = kwargs.get('status_code', None)
        self.status_detail = kwargs.get('status_detail', None)
        self.creation_time = kwargs.get('creation_time', None)
        self.end_time = kwargs.get('end_time', None)
