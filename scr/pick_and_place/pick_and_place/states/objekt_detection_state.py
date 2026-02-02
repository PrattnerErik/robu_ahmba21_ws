from __future__ import annotations
from typing import TYPE_CHECKING
from std_srvs.srv import SetBool
from geometry_msgs.msg import Pose

# Den nachfolgenden Import eventuell anpassen!
from pick_and_place.state_machine import State

if TYPE_CHECKING:
    from pick_and_place.pick_and_place_node import PickAndPlace 


class ObjectDetection(State):
    """huh?"""

    def __init__(self) -> None:
        super().__init__("OBJECT_DETECTION")

    def on_enter(self, node:PickAndPlace) -> None:
        node.get_logger().info("ENTER OBJECT_DETECTION")
        node.objekt_pose = None
        node.objekt_color = None
        node.objekt_type = None

        #TODO: Servide call -> Kamera -> moch bild -> future Objekt

    def tick(self, node:PickAndPlace) -> str | None:
        node.get_logger().info("TICK OBJECT_DETECTION")

        #TODO: warte auf future.done() == True
        #TODO: Bild verarbeiten und position, farbe und typ bestimmen
        
        node.objekt_pose = Pose()
        node.objekt_pose.position.x = 67
        node.objekt_pose.position.y = 69
        node.objekt_pose.position.z = 420
        #orientierung nicht ausgewertet -> standartwerte 0
        node.objekt_color = "glitter"
        node.objekt_type = "Wednesday"

        return "MOVE_TO_OBJECT"

    def on_exit(self, node:PickAndPlace) -> None:
        node.get_logger().info("EXIT OBJECT_DETECTION")