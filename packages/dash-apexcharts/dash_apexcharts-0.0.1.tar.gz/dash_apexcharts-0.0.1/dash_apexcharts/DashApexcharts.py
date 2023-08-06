# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashApexcharts(Component):
    """A DashApexcharts component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- curve (string; optional)

- label (string; optional):
    A label that will be printed when this component is rendered.

- options (dict; optional)

- series (list; optional):
    Dash-assigned callback that should be called to report property
    changes  to Dash, to make them available for callbacks.

- type (string; optional):
    The ID used to identify this component in Dash callbacks.

- xaxis (list; optional):
    Dash-assigned callback that should be called to report property
    changes  to Dash, to make them available for callbacks."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, label=Component.UNDEFINED, type=Component.UNDEFINED, xaxis=Component.UNDEFINED, series=Component.UNDEFINED, curve=Component.UNDEFINED, options=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'curve', 'label', 'options', 'series', 'type', 'xaxis']
        self._type = 'DashApexcharts'
        self._namespace = 'dash_apexcharts'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'curve', 'label', 'options', 'series', 'type', 'xaxis']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashApexcharts, self).__init__(**args)
