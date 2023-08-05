# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class RealTimeEndpointInfo(Model):
    """RealTimeEndpointInfo.

    :param web_service_inputs:
    :type web_service_inputs: list[~designer.models.WebServicePort]
    :param web_service_outputs:
    :type web_service_outputs: list[~designer.models.WebServicePort]
    :param deployments_info:
    :type deployments_info: list[~designer.models.DeploymentInfo]
    """

    _attribute_map = {
        'web_service_inputs': {'key': 'webServiceInputs', 'type': '[WebServicePort]'},
        'web_service_outputs': {'key': 'webServiceOutputs', 'type': '[WebServicePort]'},
        'deployments_info': {'key': 'deploymentsInfo', 'type': '[DeploymentInfo]'},
    }

    def __init__(self, *, web_service_inputs=None, web_service_outputs=None, deployments_info=None, **kwargs) -> None:
        super(RealTimeEndpointInfo, self).__init__(**kwargs)
        self.web_service_inputs = web_service_inputs
        self.web_service_outputs = web_service_outputs
        self.deployments_info = deployments_info
