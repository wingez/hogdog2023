import time

from automation.sequencer import console, temp_sensor
from automation.sequencer.graph import State, Transition, DelayGuard, PrintAction, run, MultiAction, AndGuard, Guard, \
    OrGuard, OpenGuard
from automation.sequencer import digital_io, servo_control, inventory

arm_up_down_speed = 0.3


def arm_down_transition(guard: Guard, continuation_state: State) -> Transition:
    move_down_state = State("move arm down")

    move_down_state.add_transition(Transition(
        state=continuation_state,
        guard=OrGuard(digital_io.ButtonPressed(digital_io.Inputs.arm_bot), DelayGuard(6)) & DelayGuard(2.5),
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
        guard=OrGuard(digital_io.ButtonPressed(digital_io.Inputs.arm_top), DelayGuard(6)) & DelayGuard(2.5),
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

    # transitions regarding refill

    for hogdog_type, input, output in [
        (inventory.HogDogType.Veg, digital_io.Inputs.load2, digital_io.Outputs.led2),
        (inventory.HogDogType.Meat, digital_io.Inputs.load1, digital_io.Outputs.led1),
    ]:
        # Turn on led if refill needed
        idle.add_transition(Transition(
            idle,
            guard=inventory.HasType(hogdog_type).inverse() & digital_io.LEDState(output, False),
            action=digital_io.LEDSet(output, True)
        ))
        # Refill if button pressed
        idle.add_transition(Transition(
            idle,
            guard=digital_io.ButtonPressed(input),
            action=inventory.Refill(hogdog_type) + digital_io.LEDSet(output, False)
        ))

    # state for waiting above selected hogdog, before picking up
    wait_above_pickup = State("wait_above_pickup")
    # state for waiting above selected hogdog, with hogdog on stick
    wait_above_pickup2 = State("wait_above_pickup2")

    # add transitions for all available spaces
    for hogdog_type, hogdog_place in inventory.all_places():

        switch_at_correct_type: Guard
        if hogdog_type == inventory.HogDogType.Veg:
            switch_at_correct_type = digital_io.ButtonNotPressed(digital_io.Inputs.kveg)
        elif hogdog_type == inventory.HogDogType.Meat:
            switch_at_correct_type = digital_io.ButtonPressed(digital_io.Inputs.kveg)
        else:
            raise AssertionError()

        idle.add_transition(Transition(wait_above_pickup,
                                       guard=digital_io.ButtonPressed(
                                           digital_io.Inputs.start) & switch_at_correct_type & inventory.HasHogDog(
                                           hogdog_type, hogdog_place),
                                       action=inventory.MoveToHogDog(hogdog_type, hogdog_place) + inventory.PickUp(
                                           hogdog_type, hogdog_place)
                                       ))

    wait_above_pickup.add_transition(
        arm_up_down_transition(
            guard=servo_control.ServoIdle(servo_control.upper_servo),
            move_up_guard=DelayGuard(2),
            continuation_state=wait_above_pickup2,
        ))

    wait_above_heat = State("wait_above_heat")
    wait_above_heat2 = State("wait_above_heat2")

   #wait_above_pickup2.add_transition(Transition(
   #    idle,
   #    guard=OpenGuard(),
   #    action=MultiAction(),
   #))

    wait_above_pickup2.add_transition(Transition(
        state=wait_above_heat,
        guard=OpenGuard(),
        action=servo_control.SmoothServoAngle(servo_control.upper_servo, 161)
    ))

    wait_above_heat.add_transition(arm_up_down_transition(
        guard=servo_control.ServoIdle(servo_control.upper_servo),
        move_up_guard=DelayGuard(60) | digital_io.ButtonPressed(digital_io.Inputs.start),
        continuation_state=wait_above_heat2
    ))

    wait_above_bread = State("wait above bread")

    wait_above_heat2.add_transition(Transition(
        state=wait_above_bread,
        guard=OpenGuard(),
        action=MultiAction(
            servo_control.SmoothServoAngle(servo_control.upper_servo, 0),
            servo_control.SmoothServoAngle(servo_control.lower_servo, 52)
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
            servo_control.SmoothServoAngle(servo_control.upper_servo, 13),
            servo_control.SmoothServoAngle(servo_control.lower_servo, 62)
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
        action=servo_control.SmoothServoAngle(servo_control.lower_servo, 52)
    ))

    return idle


if __name__ == '__main__':
    console.start()
    digital_io.start()
    temp_sensor.start()
    servo_control.start()
    inventory.start()

    run(create_graph())
