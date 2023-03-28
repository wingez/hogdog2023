from dash import Dash, dcc, html, Input, Output
import dash_daq as daq
from adafruit_servokit import ServoKit
import time
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
    probe_button1 = 24
    #probe_button2 = 23


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
g.setup(Inputs.probe_button1, g.IN, pull_up_down=g.PUD_UP)
#g.setup(Inputs.probe_button2, g.IN, pull_up_down=g.PUD_UP)


kit = ServoKit(channels=16)

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
        label="Kött/Veg",
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
    daq.Indicator(
        id='my-indicator-probe_button1',
        label="probe_button1",
        size="40", labelPosition="bottom",

    ),
    daq.Indicator(
        id='my-indicator-probe_button2',
        label="probe_button2",
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

html.Div([
        html.Label('Servo angular'),
        dcc.Slider(
            id='my-slider',
            value=0,
            min=0,
            max=180,
            step=1,
            marks={i: '{}'.format(i) for i in range(0,181,10)},
        ), html.Div(id='servo-slider'),
    ], style={'width': '1500px', 'margin': '20px auto'}),

    dcc.Interval(interval=1000, id="thermometer_interval"),
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
        Output('my-indicator-probe_button1', 'value'),
        #Output('my-indicator-probe_button2', 'value'),
    ],
    Input("interval", "n_intervals")
)
def read_switches(n_intervals):
    input_pins = [Inputs.start, Inputs.kveg, Inputs.ketchup, Inputs.mayo, Inputs.load1, Inputs.load2, Inputs.probe_button1]

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

@app.callback(
    Output('servo-slider', 'children'),
    Input('my-slider', 'value')
)
def update_output(value):
    print(f"Callback servo, value: {value} degrees")
    kit.servo[0].angle = value
    return 'You have selected "{}"'.format(value)


def callback_probe_button1(channel):
    #time.sleep(0.1)
    print("falling edge detected on 24")

def callback_probe_button2(channel):
    print("falling edge detected on 23")
# when a falling edge is detected on port 24/23, regardless of whatever
# else is happening in the program, the function my_callback will be run
g.add_event_detect(24, g.FALLING, callback=callback_probe_button1, bouncetime=300)
#g.add_event_detect(23, g.FALLING, callback=callback_probe_button2, bouncetime=300)

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0")
