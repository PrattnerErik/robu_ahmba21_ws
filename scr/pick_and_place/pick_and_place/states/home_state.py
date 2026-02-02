from __future__ import annotations
from typing import TYPE_CHECKING

# Den nachfolgenden Import eventuell anpassen!
from pick_and_place.state_machine import State

if TYPE_CHECKING:
    from pick_and_place.pick_and_place_node import PickAndPlace 

class Home(State):
    """Robot goes to Homing Position"""

    def __init__(self) -> None:
        super().__init__("HOME")

    def on_enter(self, node:PickAndPlace) -> None:
        node.get_logger().info("ENTER HOME")

    def tick(self, node:PickAndPlace) -> str | None:
        node.get_logger().info("TICK HOME")
        #TODO: Move-it programm
        return "CONVEYOR_BELT_START"
    
    def on_exit(self, node:PickAndPlace) -> None:
        node.get_logger().info("EXIT HOME")