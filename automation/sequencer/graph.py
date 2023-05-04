from __future__ import annotations

import time
from dataclasses import dataclass

import logging
from datetime import datetime, timedelta
from typing import List

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class State():
    def __init__(self, name: str):
        self.name = name
        self.transitions: List[Transition] = []

    def add_transition(self, transition: Transition):
        self.transitions.append(transition)

    def __str__(self):
        return self.name


class Guard:

    def __init__(self):
        pass

    def initialize(self):
        pass

    def evaluate(self) -> bool:
        raise NotImplementedError()

    def inverse(self) -> InverseGuard:
        return InverseGuard(self)

    def __and__(self, other):
        if not isinstance(other, Guard):
            return NotImplemented
        return AndGuard(self, other)

    def __or__(self, other):
        if not isinstance(other, Guard):
            return NotImplemented
        return OrGuard(self, other)


class OpenGuard(Guard):
    def evaluate(self) -> bool:
        return True


class InverseGuard(Guard):
    def __init__(self, base: Guard):
        super().__init__()
        self.base = base

    def initialize(self):
        self.base.initialize()

    def evaluate(self) -> bool:
        return not self.base.evaluate()


class OrGuard(Guard):
    def __init__(self, *bases: Guard):
        super(OrGuard, self).__init__()
        self.bases = bases

    def initialize(self):
        for base in self.bases:
            base.initialize()

    def evaluate(self) -> bool:
        return any(base.evaluate() for base in self.bases)


class AndGuard(Guard):
    def __init__(self, *bases: Guard):
        super(AndGuard, self).__init__()
        self.bases = bases

    def initialize(self):
        for base in self.bases:
            base.initialize()

    def evaluate(self) -> bool:
        return all(base.evaluate() for base in self.bases)


class Action:
    def __init__(self):
        pass

    def execute(self):
        pass


class MultiAction(Action):
    def __init__(self, *actions: Action):
        super(MultiAction, self).__init__()
        self.actions = actions

    def execute(self):
        for action in self.actions:
            action.execute()


@dataclass
class Transition:
    state: State
    guard: Guard
    action: Action

    def initialize(self):
        self.guard.initialize()


class PrintAction(Action):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def execute(self):
        logging.log(logging.INFO, self.message)


class DelayGuard(Guard):
    def __init__(self, seconds: float):
        super().__init__()
        self.seconds = seconds
        self.entry_time = datetime.now()

    def initialize(self):
        self.entry_time = datetime.now()

    def evaluate(self) -> bool:
        now = datetime.now()
        return now > self.entry_time + timedelta(seconds=self.seconds)


def run(initial_state: State):
    state = initial_state
    while True:
        logging.log(logging.INFO, f'new state is: {state}')

        for transition in state.transitions:
            transition.initialize()

        should_run = True

        while should_run:
            for transition in state.transitions:
                if transition.guard.evaluate():
                    transition.action.execute()
                    state = transition.state
                    should_run = False
                    break

            time.sleep(0.01)
