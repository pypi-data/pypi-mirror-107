# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class AKSAdvanceSettings(Model):
    """AKSAdvanceSettings.

    :param auto_scaler:
    :type auto_scaler: ~designer.models.AutoScaler
    :param container_resource_requirements:
    :type container_resource_requirements:
     ~designer.models.ContainerResourceRequirements
    :param app_insights_enabled:
    :type app_insights_enabled: bool
    :param scoring_timeout_ms:
    :type scoring_timeout_ms: int
    :param num_replicas:
    :type num_replicas: int
    """

    _attribute_map = {
        'auto_scaler': {'key': 'autoScaler', 'type': 'AutoScaler'},
        'container_resource_requirements': {'key': 'containerResourceRequirements', 'type': 'ContainerResourceRequirements'},
        'app_insights_enabled': {'key': 'appInsightsEnabled', 'type': 'bool'},
        'scoring_timeout_ms': {'key': 'scoringTimeoutMs', 'type': 'int'},
        'num_replicas': {'key': 'numReplicas', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(AKSAdvanceSettings, self).__init__(**kwargs)
        self.auto_scaler = kwargs.get('auto_scaler', None)
        self.container_resource_requirements = kwargs.get('container_resource_requirements', None)
        self.app_insights_enabled = kwargs.get('app_insights_enabled', None)
        self.scoring_timeout_ms = kwargs.get('scoring_timeout_ms', None)
        self.num_replicas = kwargs.get('num_replicas', None)
