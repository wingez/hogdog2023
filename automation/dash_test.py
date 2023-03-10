from dash import Dash, dcc, html, Input, Output
import dash_daq as daq

import RPi.GPIO as g

from thermocoupler import MAX31855


class Outputs:
    led1 = 26
    led2 = 16
    led3 = 19


class Inputs:
    start = 21
    kveg = 7
    ketchup = 6
    mayo = 13
    load1 = 5
    load2 = 12


thermometer = MAX31855(11, 10, 9)

g.setmode(g.BCM)

g.setup(Outputs.led1, g.OUT)
g.setup(Outputs.led2, g.OUT)
g.setup(Outputs.led3, g.OUT)

g.setup(Inputs.start, g.IN, pull_up_down=g.PUD_UP)
g.setup(Inputs.kveg, g.IN, pull_up_down=g.PUD_UP)
g.setup(Inputs.ketchup, g.IN, pull_up_down=g.PUD_UP)
g.setup(Inputs.mayo, g.IN, pull_up_down=g.PUD_UP)
g.setup(Inputs.load1, g.IN, pull_up_down=g.PUD_UP)
g.setup(Inputs.load2, g.IN, pull_up_down=g.PUD_UP)

app = Dash(__name__)

app.layout = html.Div([
    html.H6("Change the value in the text box to see callbacks in action!"),
    dcc.Interval(interval=200, id="interval"),
    html.Div([
        "Input: ",
        dcc.Input(id='my-input', value='initial value', type='text')
    ]),
    html.Br(),
    html.Div(id='my-output'),
    daq.BooleanSwitch(
        id='my-toggle-switch1',
        on=False,
        label="Led1",
        labelPosition="bottom",
    ),
    daq.BooleanSwitch(
        id='my-toggle-switch2',
        on=False,
        label="Led2",
        labelPosition="bottom",

    ),
    daq.BooleanSwitch(
        id='my-toggle-switch3',
        on=False,
        label="Led3", labelPosition="bottom",

    ),
    daq.Indicator(
        id='my-indicator-start',
        label="Start",
        size="40", labelPosition="bottom",

    ),
    daq.Indicator(
        id='my-indicator-kveg',
        label="kveg",
        size="40", labelPosition="bottom",

    ),
    daq.Indicator(
        id='my-indicator-ketchup',
        label="ketchup",
        size="40", labelPosition="bottom",

    ),
    daq.Indicator(
        id='my-indicator-mayo',
        label="mayo",
        size="40", labelPosition="bottom",

    ),
    daq.Indicator(
        id='my-indicator-load1',
        label="load1",
        size="40", labelPosition="bottom",

    ),
    daq.Indicator(
        id='my-indicator-load2',
        label="load2",
        size="40", labelPosition="bottom",

    ),
    daq.Thermometer(
        id='my-thermometer-1',
        value=5,
        min=0,
        max=100,
        style={
            'margin-bottom': '5%'
        },
        showCurrentValue=True,
    ),
    dcc.Interval(interval=1000, id="thermometer_interval")

])


def to_gpio_output(value):
    if value:
        return g.HIGH
    else:
        return g.LOW


@app.callback(
    Output('my-output', 'children'),
    [
        Input('my-toggle-switch1', 'on'),
        Input('my-toggle-switch2', 'on'),
        Input('my-toggle-switch3', 'on'),
    ]
)
def update_output(switch1, switch2, switch3):
    print(switch1)
    print(type(switch1))
    g.output(Outputs.led1, to_gpio_output(switch1))
    g.output(Outputs.led2, to_gpio_output(switch2))
    g.output(Outputs.led3, to_gpio_output(switch3))

    return str(any([switch1, switch2, switch3]))


@app.callback(
    [
        Output('my-indicator-start', 'value'),
        Output('my-indicator-kveg', 'value'),
        Output('my-indicator-ketchup', 'value'),
        Output('my-indicator-mayo', 'value'),
        Output('my-indicator-load1', 'value'),
        Output('my-indicator-load2', 'value'),
    ],
    Input("interval", "n_intervals")
)
def read_switches(n_intervals):
    input_pins = [Inputs.start, Inputs.kveg, Inputs.ketchup, Inputs.mayo, Inputs.load1, Inputs.load2]

    outputs = []

    for pin in input_pins:
        outputs.append(not g.input(pin))

    return outputs


@app.callback(
    Output('my-thermometer-1', 'value'),
    Input("thermometer_interval", "n_intervals")
)
def thermo_callback(n_intervals):
    return float(thermometer.get())


if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
