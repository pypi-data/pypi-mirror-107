# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PipelineDraft(Model):
    """PipelineDraft.

    :param graph_draft_id:
    :type graph_draft_id: str
    :param latest_pipeline_run_id:
    :type latest_pipeline_run_id: str
    :param latest_run_experiment_name:
    :type latest_run_experiment_name: str
    :param latest_run_experiment_id:
    :type latest_run_experiment_id: str
    :param is_latest_run_experiment_archived:
    :type is_latest_run_experiment_archived: bool
    :param status:
    :type status: ~designer.models.PipelineStatus
    :param graph_detail:
    :type graph_detail: ~designer.models.PipelineRunGraphDetail
    :param real_time_endpoint_info:
    :type real_time_endpoint_info: ~designer.models.RealTimeEndpointInfo
    :param linked_pipelines_info:
    :type linked_pipelines_info: list[~designer.models.LinkedPipelineInfo]
    :param nodes_in_draft:
    :type nodes_in_draft: list[str]
    :param studio_migration_info:
    :type studio_migration_info: ~designer.models.StudioMigrationInfo
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
        'graph_draft_id': {'key': 'graphDraftId', 'type': 'str'},
        'latest_pipeline_run_id': {'key': 'latestPipelineRunId', 'type': 'str'},
        'latest_run_experiment_name': {'key': 'latestRunExperimentName', 'type': 'str'},
        'latest_run_experiment_id': {'key': 'latestRunExperimentId', 'type': 'str'},
        'is_latest_run_experiment_archived': {'key': 'isLatestRunExperimentArchived', 'type': 'bool'},
        'status': {'key': 'status', 'type': 'PipelineStatus'},
        'graph_detail': {'key': 'graphDetail', 'type': 'PipelineRunGraphDetail'},
        'real_time_endpoint_info': {'key': 'realTimeEndpointInfo', 'type': 'RealTimeEndpointInfo'},
        'linked_pipelines_info': {'key': 'linkedPipelinesInfo', 'type': '[LinkedPipelineInfo]'},
        'nodes_in_draft': {'key': 'nodesInDraft', 'type': '[str]'},
        'studio_migration_info': {'key': 'studioMigrationInfo', 'type': 'StudioMigrationInfo'},
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
        super(PipelineDraft, self).__init__(**kwargs)
        self.graph_draft_id = kwargs.get('graph_draft_id', None)
        self.latest_pipeline_run_id = kwargs.get('latest_pipeline_run_id', None)
        self.latest_run_experiment_name = kwargs.get('latest_run_experiment_name', None)
        self.latest_run_experiment_id = kwargs.get('latest_run_experiment_id', None)
        self.is_latest_run_experiment_archived = kwargs.get('is_latest_run_experiment_archived', None)
        self.status = kwargs.get('status', None)
        self.graph_detail = kwargs.get('graph_detail', None)
        self.real_time_endpoint_info = kwargs.get('real_time_endpoint_info', None)
        self.linked_pipelines_info = kwargs.get('linked_pipelines_info', None)
        self.nodes_in_draft = kwargs.get('nodes_in_draft', None)
        self.studio_migration_info = kwargs.get('studio_migration_info', None)
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
