# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class RCranPackage(Model):
    """RCranPackage.

    :param name:
    :type name: str
    :param version:
    :type version: str
    :param repository:
    :type repository: str
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'version': {'key': 'version', 'type': 'str'},
        'repository': {'key': 'repository', 'type': 'str'},
    }

    def __init__(self, *, name: str=None, version: str=None, repository: str=None, **kwargs) -> None:
        super(RCranPackage, self).__init__(**kwargs)
        self.name = name
        self.version = version
        self.repository = repository
