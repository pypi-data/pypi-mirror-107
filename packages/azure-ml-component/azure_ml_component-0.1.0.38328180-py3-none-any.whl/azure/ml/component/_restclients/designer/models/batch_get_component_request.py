# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BatchGetComponentRequest(Model):
    """BatchGetComponentRequest.

    :param version_ids:
    :type version_ids: list[str]
    :param name_and_versions:
    :type name_and_versions: list[~designer.models.ComponentNameMetaInfo]
    """

    _attribute_map = {
        'version_ids': {'key': 'versionIds', 'type': '[str]'},
        'name_and_versions': {'key': 'nameAndVersions', 'type': '[ComponentNameMetaInfo]'},
    }

    def __init__(self, **kwargs):
        super(BatchGetComponentRequest, self).__init__(**kwargs)
        self.version_ids = kwargs.get('version_ids', None)
        self.name_and_versions = kwargs.get('name_and_versions', None)
