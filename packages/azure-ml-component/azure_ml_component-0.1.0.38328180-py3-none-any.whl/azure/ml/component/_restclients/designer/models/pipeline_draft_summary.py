# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PipelineDraftSummary(Model):
    """PipelineDraftSummary.

    :param name:
    :type name: str
    :param last_edited_by:
    :type last_edited_by: str
    :param created_by:
    :type created_by: str
    :param description:
    :type description: str
    :param pipeline_type: Possible values include: 'TrainingPipeline',
     'RealTimeInferencePipeline', 'BatchInferencePipeline', 'Unknown'
    :type pipeline_type: str or ~designer.models.PipelineType
    :param pipeline_draft_mode: Possible values include: 'None', 'Normal',
     'Custom'
    :type pipeline_draft_mode: str or ~designer.models.PipelineDraftMode
    :param tags: This is a dictionary
    :type tags: dict[str, str]
    :param properties: This is a dictionary
    :type properties: dict[str, str]
    :param entity_status: Possible values include: 'Active', 'Deprecated',
     'Disabled'
    :type entity_status: str or ~designer.models.EntityStatus
    :param id:
    :type id: str
    :param etag:
    :type etag: str
    :param created_date:
    :type created_date: datetime
    :param last_modified_date:
    :type last_modified_date: datetime
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'last_edited_by': {'key': 'lastEditedBy', 'type': 'str'},
        'created_by': {'key': 'createdBy', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'pipeline_type': {'key': 'pipelineType', 'type': 'str'},
        'pipeline_draft_mode': {'key': 'pipelineDraftMode', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
        'properties': {'key': 'properties', 'type': '{str}'},
        'entity_status': {'key': 'entityStatus', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'etag': {'key': 'etag', 'type': 'str'},
        'created_date': {'key': 'createdDate', 'type': 'iso-8601'},
        'last_modified_date': {'key': 'lastModifiedDate', 'type': 'iso-8601'},
    }

    def __init__(self, **kwargs):
        super(PipelineDraftSummary, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.last_edited_by = kwargs.get('last_edited_by', None)
        self.created_by = kwargs.get('created_by', None)
        self.description = kwargs.get('description', None)
        self.pipeline_type = kwargs.get('pipeline_type', None)
        self.pipeline_draft_mode = kwargs.get('pipeline_draft_mode', None)
        self.tags = kwargs.get('tags', None)
        self.properties = kwargs.get('properties', None)
        self.entity_status = kwargs.get('entity_status', None)
        self.id = kwargs.get('id', None)
        self.etag = kwargs.get('etag', None)
        self.created_date = kwargs.get('created_date', None)
        self.last_modified_date = kwargs.get('last_modified_date', None)
