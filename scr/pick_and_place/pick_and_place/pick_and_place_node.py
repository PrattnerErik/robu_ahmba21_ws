from rclpy.node import Node
import rclpy
from std_msgs.msg import Bool
from std_srvs.srv import SetBool
from geometry_msgs.msg import Pose

from pick_and_place.state_machine import State, StateMachine
from pick_and_place.states.initialize_state import Initialize
from pick_and_place.states.home_state import Home
from pick_and_place.states.wait_for_object_state import WaitForObject
from pick_and_place.states.conveyor_belt_start_state import ConveryorBeltStart
from pick_and_place.states.conveyor_belt_stop_state import ConveryorBeltStop
from pick_and_place.states.objekt_detection_state import ObjectDetection
from pick_and_place.states.move_to_object_state import MoveToObject


class PickAndPlace(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        #1.) Schnittstelle zur Statemashine
        self.light_barrier_detected = False
        self.vacuum_ok = False
        self.objekt_pose:Pose|None = None
        self.objekt_color:str|None = None
        self.objekt_type:str|None = None
        #...

        #2.) ROS
        # - Publisher/Subscriber
        self._sub_light_barrier_detected = self.create_subscription(Bool,
                                                                    "light_barrier_detected",
                                                                    self._sub_light_barrier_detected_cb,
                                                                    10)
        self._sub_vacuum_ok = self.create_subscription(Bool,
                                                        "vacuum_ok",
                                                        self._sub_vacuum_ok_cb,
                                                        10)
        # - Service Client
        self.cli_conveyor_belt = self.create_client(SetBool, "conveyor_belt")
        # TODO: ActionClient für Move it -> inverse Kinematik lösen

        #3.) Zustandsautomaten anlegen
        self._sm = StateMachine(self)

        #4.) Zustände anlegen
        self._sm.add_state(Initialize())
        self._sm.add_state(Home())
        self._sm.add_state(WaitForObject())
        self._sm.add_state(ConveryorBeltStart())
        self._sm.add_state(ConveryorBeltStop())
        self._sm.add_state(ObjectDetection())
        self._sm.add_state(MoveToObject())
        # TODO: more states...
        self._sm.set_initial_state("INITIALIZE")

        #5.) Timer zur Steuerung der Zustände erzeugen
        self._timer_sm = self.create_timer(0.050, self._timer_sm_cb)

    def _timer_sm_cb(self):
        self._sm.step()

    def _sub_light_barrier_detected_cb(self, msg:Bool):
        self.light_barrier_detected = msg.data

    def _sub_vacuum_ok_cb(self, msg:Bool):
        self.vacuum_ok = msg.data

    def destroy_node(self):
        return super().destroy_node()

def main():
    node = None
    try:
        rclpy.init()
        try:
            node = PickAndPlace("pick_and_place_node")
        except Exception as e:
            print(f"Fehler beim Erstellen des Nodes: {e}")
            return

        rclpy.spin(node)

    except KeyboardInterrupt:
        print("Sie haben STRG+C gedrückt!")

    finally:
        if node is not None:
            if rclpy.ok():
                node.get_logger().info(f"Node {node.get_name()} wird beendet!")
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()