# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class RealTimeEndpoint(Model):
    """RealTimeEndpoint.

    :param created_by:
    :type created_by: str
    :param kv_tags:
    :type kv_tags: dict[str, str]
    :param state: Possible values include: 'Transitioning', 'Healthy',
     'Unhealthy', 'Failed', 'Unschedulable'
    :type state: str or ~designer.models.WebServiceState
    :param error:
    :type error: ~designer.models.ModelManagementErrorResponse
    :param compute_type: Possible values include: 'ACI', 'AKS', 'AMLCOMPUTE',
     'IOT', 'AKSENDPOINT', 'MIRSINGLEMODEL', 'MIRAMLCOMPUTE', 'UNKNOWN'
    :type compute_type: str or ~designer.models.ComputeEnvironmentType
    :param image_id:
    :type image_id: str
    :param cpu:
    :type cpu: float
    :param memory_in_gb:
    :type memory_in_gb: float
    :param max_concurrent_requests_per_container:
    :type max_concurrent_requests_per_container: int
    :param num_replicas:
    :type num_replicas: int
    :param event_hub_enabled:
    :type event_hub_enabled: bool
    :param storage_enabled:
    :type storage_enabled: bool
    :param app_insights_enabled:
    :type app_insights_enabled: bool
    :param auto_scale_enabled:
    :type auto_scale_enabled: bool
    :param min_replicas:
    :type min_replicas: int
    :param max_replicas:
    :type max_replicas: int
    :param target_utilization:
    :type target_utilization: int
    :param refresh_period_in_seconds:
    :type refresh_period_in_seconds: int
    :param scoring_uri:
    :type scoring_uri: str
    :param deployment_status:
    :type deployment_status: ~designer.models.AKSReplicaStatus
    :param scoring_timeout_ms:
    :type scoring_timeout_ms: int
    :param auth_enabled:
    :type auth_enabled: bool
    :param aad_auth_enabled:
    :type aad_auth_enabled: bool
    :param region:
    :type region: str
    :param primary_key:
    :type primary_key: str
    :param secondary_key:
    :type secondary_key: str
    :param swagger_uri:
    :type swagger_uri: str
    :param linked_pipeline_draft_id:
    :type linked_pipeline_draft_id: str
    :param linked_pipeline_run_id:
    :type linked_pipeline_run_id: str
    :param warning:
    :type warning: str
    :param name:
    :type name: str
    :param description:
    :type description: str
    :param id:
    :type id: str
    :param created_time:
    :type created_time: datetime
    :param updated_time:
    :type updated_time: datetime
    :param compute_name:
    :type compute_name: str
    :param updated_by:
    :type updated_by: str
    """

    _attribute_map = {
        'created_by': {'key': 'createdBy', 'type': 'str'},
        'kv_tags': {'key': 'kvTags', 'type': '{str}'},
        'state': {'key': 'state', 'type': 'str'},
        'error': {'key': 'error', 'type': 'ModelManagementErrorResponse'},
        'compute_type': {'key': 'computeType', 'type': 'str'},
        'image_id': {'key': 'imageId', 'type': 'str'},
        'cpu': {'key': 'cpu', 'type': 'float'},
        'memory_in_gb': {'key': 'memoryInGB', 'type': 'float'},
        'max_concurrent_requests_per_container': {'key': 'maxConcurrentRequestsPerContainer', 'type': 'int'},
        'num_replicas': {'key': 'numReplicas', 'type': 'int'},
        'event_hub_enabled': {'key': 'eventHubEnabled', 'type': 'bool'},
        'storage_enabled': {'key': 'storageEnabled', 'type': 'bool'},
        'app_insights_enabled': {'key': 'appInsightsEnabled', 'type': 'bool'},
        'auto_scale_enabled': {'key': 'autoScaleEnabled', 'type': 'bool'},
        'min_replicas': {'key': 'minReplicas', 'type': 'int'},
        'max_replicas': {'key': 'maxReplicas', 'type': 'int'},
        'target_utilization': {'key': 'targetUtilization', 'type': 'int'},
        'refresh_period_in_seconds': {'key': 'refreshPeriodInSeconds', 'type': 'int'},
        'scoring_uri': {'key': 'scoringUri', 'type': 'str'},
        'deployment_status': {'key': 'deploymentStatus', 'type': 'AKSReplicaStatus'},
        'scoring_timeout_ms': {'key': 'scoringTimeoutMs', 'type': 'int'},
        'auth_enabled': {'key': 'authEnabled', 'type': 'bool'},
        'aad_auth_enabled': {'key': 'aadAuthEnabled', 'type': 'bool'},
        'region': {'key': 'region', 'type': 'str'},
        'primary_key': {'key': 'primaryKey', 'type': 'str'},
        'secondary_key': {'key': 'secondaryKey', 'type': 'str'},
        'swagger_uri': {'key': 'swaggerUri', 'type': 'str'},
        'linked_pipeline_draft_id': {'key': 'linkedPipelineDraftId', 'type': 'str'},
        'linked_pipeline_run_id': {'key': 'linkedPipelineRunId', 'type': 'str'},
        'warning': {'key': 'warning', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'description': {'key': 'description', 'type': 'str'},
        'id': {'key': 'id', 'type': 'str'},
        'created_time': {'key': 'createdTime', 'type': 'iso-8601'},
        'updated_time': {'key': 'updatedTime', 'type': 'iso-8601'},
        'compute_name': {'key': 'computeName', 'type': 'str'},
        'updated_by': {'key': 'updatedBy', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(RealTimeEndpoint, self).__init__(**kwargs)
        self.created_by = kwargs.get('created_by', None)
        self.kv_tags = kwargs.get('kv_tags', None)
        self.state = kwargs.get('state', None)
        self.error = kwargs.get('error', None)
        self.compute_type = kwargs.get('compute_type', None)
        self.image_id = kwargs.get('image_id', None)
        self.cpu = kwargs.get('cpu', None)
        self.memory_in_gb = kwargs.get('memory_in_gb', None)
        self.max_concurrent_requests_per_container = kwargs.get('max_concurrent_requests_per_container', None)
        self.num_replicas = kwargs.get('num_replicas', None)
        self.event_hub_enabled = kwargs.get('event_hub_enabled', None)
        self.storage_enabled = kwargs.get('storage_enabled', None)
        self.app_insights_enabled = kwargs.get('app_insights_enabled', None)
        self.auto_scale_enabled = kwargs.get('auto_scale_enabled', None)
        self.min_replicas = kwargs.get('min_replicas', None)
        self.max_replicas = kwargs.get('max_replicas', None)
        self.target_utilization = kwargs.get('target_utilization', None)
        self.refresh_period_in_seconds = kwargs.get('refresh_period_in_seconds', None)
        self.scoring_uri = kwargs.get('scoring_uri', None)
        self.deployment_status = kwargs.get('deployment_status', None)
        self.scoring_timeout_ms = kwargs.get('scoring_timeout_ms', None)
        self.auth_enabled = kwargs.get('auth_enabled', None)
        self.aad_auth_enabled = kwargs.get('aad_auth_enabled', None)
        self.region = kwargs.get('region', None)
        self.primary_key = kwargs.get('primary_key', None)
        self.secondary_key = kwargs.get('secondary_key', None)
        self.swagger_uri = kwargs.get('swagger_uri', None)
        self.linked_pipeline_draft_id = kwargs.get('linked_pipeline_draft_id', None)
        self.linked_pipeline_run_id = kwargs.get('linked_pipeline_run_id', None)
        self.warning = kwargs.get('warning', None)
        self.name = kwargs.get('name', None)
        self.description = kwargs.get('description', None)
        self.id = kwargs.get('id', None)
        self.created_time = kwargs.get('created_time', None)
        self.updated_time = kwargs.get('updated_time', None)
        self.compute_name = kwargs.get('compute_name', None)
        self.updated_by = kwargs.get('updated_by', None)
