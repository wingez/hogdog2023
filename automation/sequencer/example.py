import time

from automation.sequencer import console
from automation.sequencer.graph import State, Transition, DelayGuard, PrintAction, run, MultiAction, AndGuard
from automation.sequencer import digital_io, servo_control


def create_tree() -> State:
    s1 = State("waiting")
    s2 = State("s2")
    s3 = State("s3")
    s4 = State("s4")

    s1.add_transition(Transition(
        state=s2,
        guard=digital_io.ButtonPressed(digital_io.Inputs.start),
        action=servo_control.ServoSpeed(servo_control.arm_servo, servo_control.arm_up*0.1)
    ))

    s2.add_transition(Transition(
        state=s3,
        guard=digital_io.ButtonPressed(digital_io.Inputs.arm_top),
        action=servo_control.ServoSpeed(servo_control.arm_servo, 0)
    ))

    s3.add_transition(Transition(
        state=s4,
        guard=DelayGuard(2),
        action=servo_control.ServoSpeed(servo_control.arm_servo, servo_control.arm_down*0.1)
    ))

    s4.add_transition(Transition(
        state=s1,
        guard=digital_io.ButtonPressed(digital_io.Inputs.arm_bot),
        action=servo_control.ServoSpeed(servo_control.arm_servo, 0)
    ))


    return s1


    s1 = State("s1")
    s2 = State("s2")

    s1.add_transition(Transition(
        state=s2,
        guard=digital_io.ButtonPressed(digital_io.Inputs.start),
        action=servo_control.ServoSpeed(servo_control.arm_servo, -0.1)
    ))

    s2.add_transition(Transition(
        state=s1,
        guard=DelayGuard(1),  # digital_io.ButtonNotPressed(digital_io.Inputs.kveg)),
        action=servo_control.ServoSpeed(servo_control.arm_servo, 0),
    ))

    return s1

    s1 = State("s1")
    s2 = State("s2")

    s1.add_transition(Transition(
        state=s2,
        guard=AndGuard(servo_control.ServoIdle(servo_control.lower_servo),
                       digital_io.ButtonPressed(digital_io.Inputs.start)),
        action=servo_control.ServoAngle(servo_control.lower_servo, 50)
    ))

    s2.add_transition(Transition(
        state=s1,
        guard=AndGuard(servo_control.ServoIdle(servo_control.lower_servo),
                       DelayGuard(2)),  # digital_io.ButtonNotPressed(digital_io.Inputs.kveg)),
        action=servo_control.ServoAngle(servo_control.lower_servo, 40),

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
