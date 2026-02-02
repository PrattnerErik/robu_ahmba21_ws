from __future__ import annotations
from typing import TYPE_CHECKING
from std_srvs.srv import SetBool

# Den nachfolgenden Import eventuell anpassen!
from pick_and_place.state_machine import State
import time
if TYPE_CHECKING:
    from pick_and_place.pick_and_place_node import PickAndPlace 


class ConveryorBeltStop(State):
    """blablabla"""

    def __init__(self) -> None:
        super().__init__("CONVEYOR_BELT_STOP")
        self.future = None
        self.t0 = None
        self.TIMEOUT_DURATION = 10.0

    def on_enter(self, node:PickAndPlace) -> None:
        node.get_logger().info("ENTER CONVEYOR_BELT_STOP")
        self.t0 = time.time()
        self.stop_motor(node)

    def tick(self, node:PickAndPlace) -> str | None:
        node.get_logger().info("TICK CONVEYOR_BELT_STOP")
        if time.time() -self.t0 > self.TIMEOUT_DURATION:
            return "INITIALIZE"

        if self.future is None:
            self.stop_motor(node)

        if not self.future.done():
            return None
        
        response:SetBool.Response = self.future()
        if not response.success:
            self.future = None
            self.stop_motor(node)
            return None

        return "OBJECT_DETECTION"

    def on_exit(self, node:PickAndPlace) -> None:
        node.get_logger().info("EXIT CONVEYOR_BELT_STOP")

    def stop_motor(self, node:PickAndPlace):
        request = SetBool.Request()
        request.data = False
        self.future = node.cli_conveyor_belt.call_async(request)
