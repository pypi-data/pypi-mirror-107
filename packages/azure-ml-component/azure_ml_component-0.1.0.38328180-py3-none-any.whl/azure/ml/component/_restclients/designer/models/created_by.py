# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class CreatedBy(Model):
    """CreatedBy.

    :param user_object_id:
    :type user_object_id: str
    :param user_tenant_id:
    :type user_tenant_id: str
    :param user_name:
    :type user_name: str
    """

    _attribute_map = {
        'user_object_id': {'key': 'userObjectId', 'type': 'str'},
        'user_tenant_id': {'key': 'userTenantId', 'type': 'str'},
        'user_name': {'key': 'userName', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(CreatedBy, self).__init__(**kwargs)
        self.user_object_id = kwargs.get('user_object_id', None)
        self.user_tenant_id = kwargs.get('user_tenant_id', None)
        self.user_name = kwargs.get('user_name', None)
