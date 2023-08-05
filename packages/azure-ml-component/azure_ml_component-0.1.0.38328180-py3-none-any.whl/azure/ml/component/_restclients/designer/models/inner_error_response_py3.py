# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class InnerErrorResponse(Model):
    """InnerErrorResponse.

    :param code:
    :type code: str
    :param inner_error:
    :type inner_error: ~designer.models.InnerErrorResponse
    """

    _attribute_map = {
        'code': {'key': 'code', 'type': 'str'},
        'inner_error': {'key': 'innerError', 'type': 'InnerErrorResponse'},
    }

    def __init__(self, *, code: str=None, inner_error=None, **kwargs) -> None:
        super(InnerErrorResponse, self).__init__(**kwargs)
        self.code = code
        self.inner_error = inner_error
