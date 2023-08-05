# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class RunSettingUIParameterHint(Model):
    """RunSettingUIParameterHint.

    :param ui_widget_type: Possible values include: 'Default',
     'ComputeSelection', 'JsonEditor', 'Mode', 'SearchSpaceParameter',
     'SectionToggle', 'YamlEditor'
    :type ui_widget_type: str or ~designer.models.RunSettingUIWidgetTypeEnum
    :param json_editor:
    :type json_editor: ~designer.models.UIJsonEditor
    :param compute_selection:
    :type compute_selection: ~designer.models.UIComputeSelection
    :param ux_ignore:
    :type ux_ignore: bool
    :param anonymous:
    :type anonymous: bool
    """

    _attribute_map = {
        'ui_widget_type': {'key': 'uiWidgetType', 'type': 'str'},
        'json_editor': {'key': 'jsonEditor', 'type': 'UIJsonEditor'},
        'compute_selection': {'key': 'computeSelection', 'type': 'UIComputeSelection'},
        'ux_ignore': {'key': 'uxIgnore', 'type': 'bool'},
        'anonymous': {'key': 'anonymous', 'type': 'bool'},
    }

    def __init__(self, *, ui_widget_type=None, json_editor=None, compute_selection=None, ux_ignore: bool=None, anonymous: bool=None, **kwargs) -> None:
        super(RunSettingUIParameterHint, self).__init__(**kwargs)
        self.ui_widget_type = ui_widget_type
        self.json_editor = json_editor
        self.compute_selection = compute_selection
        self.ux_ignore = ux_ignore
        self.anonymous = anonymous
