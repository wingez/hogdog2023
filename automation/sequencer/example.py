import time

from automation.sequencer import console
from automation.sequencer.graph import State, Transition, DelayGuard, PrintAction, run, MultiAction
from automation.sequencer import digital_io


def create_tree() -> State:
    s1 = State("s1")
    s2 = State("s2")

    s1.add_transition(Transition(
        state=s2,
        guard=digital_io.ButtonPressed(digital_io.Inputs.probe_button1),
        action=digital_io.LEDState(digital_io.Outputs.led1, True),
    ))

    s2.add_transition(Transition(
        state=s1,
        guard=digital_io.ButtonPressed(digital_io.Inputs.probe_button2),
        action=digital_io.LEDState(digital_io.Outputs.led1, False),

    ))

    return s1

    s1 = State("s1")
    s2 = State("s2")
    s3 = State("s3")

    s1.add_transition(Transition(
        state=s2,
        guard=digital_io.ButtonPressed(digital_io.Inputs.start),
        action=MultiAction(PrintAction("transition to s2"),
                           digital_io.LEDState(digital_io.Outputs.led1, True)),
    ))

    s2.add_transition(Transition(
        state=s1,
        guard=console.KeyPressedGuard("1"),
        action=MultiAction(PrintAction("transition to s1"),
                           digital_io.LEDState(digital_io.Outputs.led1, False)),

    ))

    s2.add_transition(Transition(
        state=s3,
        guard=console.KeyPressedGuard("3"),
        action=PrintAction("transition to s3"),
    ))

    s3.add_transition(Transition(
        state=s1,
        guard=DelayGuard(3),
        action=MultiAction(PrintAction("transition to s1"),
                           digital_io.LEDState(digital_io.Outputs.led1, False))
    ))

    return s1


if __name__ == '__main__':
    console.start()
    digital_io.start()
    run(create_tree())
