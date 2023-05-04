import time

from automation.sequencer import console, temp_sensor
from automation.sequencer.graph import State, Transition, DelayGuard, PrintAction, run, MultiAction, AndGuard, Guard, \
    OrGuard, OpenGuard
from automation.sequencer import digital_io, servo_control

arm_up_down_speed = 0.3


def arm_down_transition(guard: Guard, continuation_state: State) -> Transition:
    move_down_state = State("move arm down")

    move_down_state.add_transition(Transition(
        state=continuation_state,
        guard=OrGuard(digital_io.ButtonPressed(digital_io.Inputs.arm_bot), DelayGuard(3)),
        action=servo_control.ServoSpeed(servo_control.arm_servo, 0)
    ))

    return Transition(
        state=move_down_state,
        guard=guard,
        action=servo_control.ServoSpeed(servo_control.arm_servo, arm_up_down_speed * servo_control.arm_down)
    )


def arm_up_transition(guard: Guard, continuation_state: State) -> Transition:
    move_up_state = State("move arm down")

    move_up_state.add_transition(Transition(
        state=continuation_state,
        guard=OrGuard(digital_io.ButtonPressed(digital_io.Inputs.arm_top), DelayGuard(3)),
        action=servo_control.ServoSpeed(servo_control.arm_servo, 0)
    ))

    return Transition(
        state=move_up_state,
        guard=guard,
        action=servo_control.ServoSpeed(servo_control.arm_servo, arm_up_down_speed * servo_control.arm_up)
    )


def arm_up_down_transition(guard: Guard, move_up_guard: Guard, continuation_state: State) -> Transition:
    wait_at_bottom = State("wait_at_bottom")

    wait_at_bottom.add_transition(arm_up_transition(move_up_guard, continuation_state))

    return arm_down_transition(guard, wait_at_bottom)


def create_graph() -> State:
    idle = State("idle")

    wait_above_pickup = State("wait_above_pickup")

    wait_above_pickup2 = State("wait_above_pickup2")
    idle.add_transition(Transition(wait_above_pickup,
                                   guard=digital_io.ButtonPressed(digital_io.Inputs.start),
                                   action=servo_control.ServoAngle(servo_control.upper_servo, 31)))

    wait_above_pickup.add_transition(
        arm_up_down_transition(
            guard=servo_control.ServoIdle(servo_control.upper_servo),
            move_up_guard=DelayGuard(2),
            continuation_state=wait_above_pickup2,
        ))

    wait_above_heat = State("wait_above_heat")
    wait_above_heat2 = State("wait_above_heat2")

    wait_above_pickup2.add_transition(Transition(
        state=wait_above_heat,
        guard=OpenGuard(),
        action=servo_control.ServoAngle(servo_control.upper_servo, 160)
    ))

    wait_above_heat.add_transition(arm_up_down_transition(
        guard=servo_control.ServoIdle(servo_control.upper_servo),
        move_up_guard=DelayGuard(2),
        continuation_state=wait_above_heat2
    ))

    wait_above_bread = State("wait above bread")

    wait_above_heat2.add_transition(Transition(
        state=wait_above_bread,
        guard=OpenGuard(),
        action=MultiAction(
            servo_control.ServoAngle(servo_control.upper_servo, 0),
            servo_control.ServoAngle(servo_control.lower_servo, 49)
        )

    ))

    wait_in_bread = State("wait in bread")

    wait_above_bread.add_transition(arm_down_transition(
        guard=AndGuard(
            servo_control.ServoIdle(servo_control.upper_servo),
            servo_control.ServoIdle(servo_control.lower_servo),
        ),
        continuation_state=wait_in_bread,
    ))

    wait_below_pull = State("wait below pull")
    wait_in_bread.add_transition(Transition(
        state=wait_below_pull,
        guard=OpenGuard(),
        action=MultiAction(
            servo_control.ServoAngle(servo_control.upper_servo, 13),
            servo_control.ServoAngle(servo_control.lower_servo, 62)
        )
    ))

    pulled = State("pulled")
    wait_below_pull.add_transition(
        arm_up_transition(
            guard=AndGuard(
                servo_control.ServoIdle(servo_control.upper_servo),
                servo_control.ServoIdle(servo_control.lower_servo),
            ),
            continuation_state=pulled,
        )
    )

    pulled.add_transition(Transition(
        state=idle,
        guard=OpenGuard(),
        action=servo_control.ServoAngle(servo_control.lower_servo, 49)
    ))

    return idle


if __name__ == '__main__':
    console.start()
    digital_io.start()
    temp_sensor.start()
    run(create_graph())
