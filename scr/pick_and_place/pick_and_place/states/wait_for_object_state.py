from __future__ import annotations
from typing import TYPE_CHECKING
from std_srvs.srv import SetBool

# Den nachfolgenden Import eventuell anpassen!
from pick_and_place.state_machine import State

if TYPE_CHECKING:
    from pick_and_place.pick_and_place_node import PickAndPlace 


class WaitForObject(State):
    """wait for object"""

    def __init__(self) -> None:
        super().__init__("WAIT_FOR_OBJECT")

    def on_enter(self, node:PickAndPlace) -> None:
        node.get_logger().info("ENTER WAIT_FOR_OBJECT")

    def tick(self, node:PickAndPlace) -> str | None:
        node.get_logger().info("TICK WAIT_FOR_OBJECT")

        if not node.light_barrier_detected:
            return None

        return "CONVERYOR_BELT_STOP"

    def on_exit(self, node:PickAndPlace) -> None:
        node.get_logger().info("EXIT WAIT_FOR_OBJECT")