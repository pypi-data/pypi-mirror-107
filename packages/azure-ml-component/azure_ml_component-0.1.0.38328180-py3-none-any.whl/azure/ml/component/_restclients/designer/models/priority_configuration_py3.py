# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PriorityConfiguration(Model):
    """PriorityConfiguration.

    :param job_priority:
    :type job_priority: int
    :param is_preemptible:
    :type is_preemptible: bool
    :param node_count_set:
    :type node_count_set: list[int]
    :param scale_interval:
    :type scale_interval: int
    """

    _attribute_map = {
        'job_priority': {'key': 'jobPriority', 'type': 'int'},
        'is_preemptible': {'key': 'isPreemptible', 'type': 'bool'},
        'node_count_set': {'key': 'nodeCountSet', 'type': '[int]'},
        'scale_interval': {'key': 'scaleInterval', 'type': 'int'},
    }

    def __init__(self, *, job_priority: int=None, is_preemptible: bool=None, node_count_set=None, scale_interval: int=None, **kwargs) -> None:
        super(PriorityConfiguration, self).__init__(**kwargs)
        self.job_priority = job_priority
        self.is_preemptible = is_preemptible
        self.node_count_set = node_count_set
        self.scale_interval = scale_interval
