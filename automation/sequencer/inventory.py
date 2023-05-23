from enum import Enum
from typing import Tuple, Dict, Iterable
import itertools as it

from automation.sequencer.graph import Guard, Action
from automation.sequencer import servo_control

PLACES_PER_TYPE = 5


class HogDogType(Enum):
    Veg = 1
    Meat = 2


inventory: Dict[Tuple[HogDogType, int], bool] = {}

angles = {
    (HogDogType.Meat, 0): 31,
    (HogDogType.Meat, 1): 38,
    (HogDogType.Meat, 2): 44,
    (HogDogType.Meat, 3): 51,
    (HogDogType.Meat, 4): 58,
    (HogDogType.Veg, 0): 65,
    (HogDogType.Veg, 1): 72,
    (HogDogType.Veg, 2): 79,
    (HogDogType.Veg, 3): 85,
    (HogDogType.Veg, 4): 92,
}


def print_inventory():
    print("Inventory contents:")
    for key in sorted(inventory, key=str):
        print(key, inventory[key])


def all_places() -> Iterable[Tuple[HogDogType, int]]:
    return it.product([HogDogType.Veg, HogDogType.Meat], range(PLACES_PER_TYPE))


def start():
    for hogdog_type, place in all_places():
        inventory[(hogdog_type, place)] = False
    print_inventory()


class HasType(Guard):
    def __init__(self, type: HogDogType):
        super(HasType, self).__init__()
        self.type = type

    def evaluate(self) -> bool:
        for key, val in inventory.items():
            if key[0] == self.type and val:
                return True
        return False


class HasHogDog(Guard):
    def __init__(self, type: HogDogType, place: int):
        super(HasHogDog, self).__init__()
        self.type, self.place = type, place

    def evaluate(self) -> bool:
        return inventory[(self.type, self.place)]


class MoveToHogDog(servo_control.SmoothServoAngle):
    def __init__(self, type: HogDogType, place: int):
        angle = angles[(type, place)]

        super(MoveToHogDog, self).__init__(
            servo=servo_control.upper_servo,
            angle=angle
        )


class PickUp(Action):
    def __init__(self, type: HogDogType, place: int):
        super(PickUp, self).__init__()
        self.type, self.place = type, place

    def execute(self):
        inventory[(self.type, self.place)] = False
        print_inventory()


class Refill(Action):
    def __init__(self, type: HogDogType):
        super(Refill, self).__init__()
        self.type = type

    def execute(self):
        for key in inventory:
            if key[0] == self.type:
                inventory[key] = True
        print_inventory()
