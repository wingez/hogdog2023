import time

from automation.sequencer import console
from automation.sequencer.console import KeyPressedGuard
from automation.sequencer.graph import State, Transition, DelayGuard, PrintAction, run


def create_tree() -> State:
    s1 = State("s1")
    s2 = State("s2")
    s3 = State("s3")

    s1.add_transition(Transition(
        state=s2,
        guard=DelayGuard(2),
        action=PrintAction("transition to s2"),
    ))

    s2.add_transition(Transition(
        state=s1,
        guard=KeyPressedGuard("1"),
        action=PrintAction("transition to s1"),
    ))

    s2.add_transition(Transition(
        state=s3,
        guard=KeyPressedGuard("3"),
        action=PrintAction("transition to s3"),
    ))

    s3.add_transition(Transition(
        state=s1,
        guard=DelayGuard(3),
        action=PrintAction("transition to s1"),
    ))

    return s1


if __name__ == '__main__':
    console.start()
    run(create_tree())
