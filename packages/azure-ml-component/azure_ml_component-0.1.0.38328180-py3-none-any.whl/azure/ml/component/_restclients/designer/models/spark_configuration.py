# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class SparkConfiguration(Model):
    """SparkConfiguration.

    :param configuration:
    :type configuration: dict[str, str]
    """

    _attribute_map = {
        'configuration': {'key': 'configuration', 'type': '{str}'},
    }

    def __init__(self, **kwargs):
        super(SparkConfiguration, self).__init__(**kwargs)
        self.configuration = kwargs.get('configuration', None)
