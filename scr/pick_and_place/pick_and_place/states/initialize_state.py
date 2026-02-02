from __future__ import annotations
from typing import TYPE_CHECKING

# Den nachfolgenden Import eventuell anpassen!
from pick_and_place.state_machine import State

if TYPE_CHECKING:
    from pick_and_place.pick_and_place_node import PickAndPlace 

class Initialize(State):
    """Inizialisiert der Roboter und prüft Sensoren und Aktoren"""

    def __init__(self) -> None:
        super().__init__("INITIALIZE")

    def on_enter(self, node:PickAndPlace) -> None:
        node.get_logger().info("ENTER INITIALIZE")

    def tick(self, node:PickAndPlace) -> str | None:
        node.get_logger().info("TICK INITIALIZE")

        # wait until conveyor belt is available
        if not node.cli_conveyor_belt.service_is_ready():
            return None
        # check other functions

        # every function is available
        return "HOME"

    def on_exit(self, node:PickAndPlace) -> None:
        node.get_logger().info("EXIT INITIALIZE")