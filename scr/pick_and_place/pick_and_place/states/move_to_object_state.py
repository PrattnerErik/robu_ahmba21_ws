from __future__ import annotations
from typing import TYPE_CHECKING
from std_srvs.srv import SetBool
from geometry_msgs.msg import Pose

# Den nachfolgenden Import eventuell anpassen!
from pick_and_place.state_machine import State

if TYPE_CHECKING:
    from pick_and_place.pick_and_place_node import PickAndPlace 


class MoveToObject(State):
    """hund foat aun"""

    def __init__(self) -> None:
        super().__init__("MOVE_TO_OBJECT")

    def on_enter(self, node:PickAndPlace) -> None:
        node.get_logger().info("ENTER MOVE_TO_OBJECT")

        #TODO: objekt daten einlesen -> node.object_pose ...
        #TODO: pose an MoveIt() übergeben

    def tick(self, node:PickAndPlace) -> str | None:
        node.get_logger().info("TICK MOVE_TO_OBJECT")

        #TODO: warte bis obect erreicht ist

        return "GRAB_OBJECT"

    def on_exit(self, node:PickAndPlace) -> None:
        node.get_logger().info("EXIT MOVE_TO_OBJECT")