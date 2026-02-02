from __future__ import annotations
from typing import TYPE_CHECKING
from std_srvs.srv import SetBool

# Den nachfolgenden Import eventuell anpassen!
from pick_and_place.state_machine import State
import time
if TYPE_CHECKING:
    from pick_and_place.pick_and_place_node import PickAndPlace 


class ConveryorBeltStart(State):
    """blablabla"""

    def __init__(self) -> None:
        super().__init__("CONVEYOR_BELT_START")
        self.future = None
        self.t0 = None
        self.timeout_duration = 10.0

    def on_enter(self, node:PickAndPlace) -> None:
        node.get_logger().info("ENTER CONVEYOR_BELT_START")
        self.t0 = time.time()
        self.cli_conveyor_belt_call_async(node)

    def tick(self, node:PickAndPlace) -> str | None:
        node.get_logger().info("TICK CONVEYOR_BELT_START")
        if time.time() -self.t0 > self.timeout_duration:
            return "INITIALIZE"

        if self.future is None:
            self.cli_conveyor_belt_call_async(node)

        if not self.future.done():
            return None
        
        response:SetBool.Response = self.future()
        if not response.success:
            self.future = None
            self.cli_conveyor_belt_call_async(node)
            return None

        return "WAIT_FOR_OBJECT"

    def on_exit(self, node:PickAndPlace) -> None:
        node.get_logger().info("EXIT CONVEYOR_BELT_START")

    def cli_conveyor_belt_call_async(self, node:PickAndPlace):
        request = SetBool.Request()
        request.data = True
        self.future = node.cli_conveyor_belt.call_async(request)
