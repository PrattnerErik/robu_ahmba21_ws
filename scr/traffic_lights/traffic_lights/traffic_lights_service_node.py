from rclpy.node import Node
import rclpy
from enum import Enum

from rcl_interfaces.msg import Parameter
from std_msgs.msg import Int8
from traffic_lights_interfaces.srv import SetTrafficLightsMode

class TrafficLightsState(Enum):
    RED = 1
    YELLOW_TO_GREEN = 2
    YELLOW_FLASHING = 3
    GREEN = 4
    GREEN_FLASHING = 5
    RED_YELLOW = 6
    OFF = 7
    YELLOW_TO_RED = 8

class TrafficLightsMode(Enum):
    STANDART = 1
    STANDART_RY = 2         #rot => rot-gelb => gruen => grün-blinkend => gelb => rot
    CONSTRUCTION = 3
    MANUAL_RED = 4
    MANUAL_GREEN = 5
    MANUAL_YELLOW = 6
    OFF_FLASHING = 7
    DISCO = 8
    OFF = 9

class TrafficLightsServiceNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        #Parameter
        self.declare_parameter("duration_green", 3.0)
        self.declare_parameter("duration_red", 3.0)
        self.declare_parameter("duration_yellow", 3.0)

        self.declare_parameter("green_flashing_repetitions", 3)
        self.declare_parameter("duration_green_flashing", .5) #Blinkperiode

        self.declare_parameter("duration_yellow_flashing", .5) #Blinkperiode

        #ENUMs selber könnern nicht auf parameter gespeichert werden - nur integer, fließkomma, listen und tuples erlaubt
        # -> enum.name -> String -> ok
        self.declare_parameter("mode", TrafficLightsMode.OFF_FLASHING.name)

        #param überschreiben: ros2 run paket_name executable_name --ros-args -p duration_green:=500.0
        self._param_duration_green = self.get_parameter("duration_green").get_parameter_value().double_value
        self._param_duration_red = self.get_parameter("duration_red").get_parameter_value().double_value
        self._param_duration_yellow = self.get_parameter("duration_yellow").get_parameter_value().double_value

        self._param_green_flashing_repetitions = self.get_parameter("green_flashing_repetitions").get_parameter_value().integer_value
        self._param_duration_green_flashing = self.get_parameter("duration_green_flashing").get_parameter_value().double_value

        self._param_duration_yellow_flashing = self.get_parameter("duration_yellow_flashing").get_parameter_value().double_value

        # umwandlung notwendig -> TrafficLightsMode[schlüssel] -> gültige enum oder ERROR
        self._param_mode = TrafficLightsMode[self.get_parameter("mode").get_parameter_value().string_value]
        self._state = TrafficLightsState.OFF

        self.add_post_set_parameters_callback(self._param_update_cb)

        #publisher erstellen
        # statt TrafficLightsState Int8 weil sonnst kein standart datentyp von ros - alternativ eigene schnittstelle erstellen (interface)
        self._pub_LED_state = self.create_publisher(Int8, "/light_state", 10)
        self._lt_state = TrafficLightsState.OFF

        #service erstellen
        self.create_service(SetTrafficLightsMode, "set_traffic_lights_mode", self._srv_set_traffic_lights_mode_cb)
        self._timer_tl = self.create_timer(1.0, self._timer_tl_cb)
        

    def _srv_set_traffic_lights_mode_cb(self,
                                        request:SetTrafficLightsMode.Request,
                                        response:SetTrafficLightsMode.Response)\
                                            -> SetTrafficLightsMode.Response:
        self._mode_new = TrafficLightsMode(request.mode)
        response.success = True
        response.msg = "amelmodus übernommen"
        return response

    def _timer_tl_cb(self):
        #prüft modus -> führt modus aus
        #modi: TrafficLightsMode

        if self._param_mode == TrafficLightsMode.STANDART or \
            self._param_mode == TrafficLightsMode.STANDART_RY:

            if self._state == TrafficLightsState.OFF:
                self._state = TrafficLightsState.RED
                self._timer_tl.destroy()
                self._timer_tl = self.create_timer(self._param_duration_red,
                                                   self._timer_tl_cb)
                
            elif self._state == TrafficLightsState.RED:
                if self._param_mode == TrafficLightsMode.STANDART:
                    self._state = TrafficLightsState.YELLOW_TO_GREEN
                else:
                    self._state = TrafficLightsState.RED_YELLOW
                self._timer_tl.destroy()
                self._timer_tl = self.create_timer(self._param_duration_yellow,
                                                self._timer_tl_cb)
                
            elif self._state == TrafficLightsState.YELLOW_TO_GREEN or\
                self._state == TrafficLightsState.RED_YELLOW:
                self._state = TrafficLightsState.GREEN
                self._timer_tl.destroy()
                self._timer_tl = self.create_timer(self._param_duration_green,
                                                   self._timer_tl_cb)
                
            elif self._state == TrafficLightsState.GREEN:
                self._state = TrafficLightsState.GREEN_FLASHING
                self._counter_blink = 0
                self._timer_tl.destroy()
                self._timer_tl = self.create_timer(self._param_duration_green_flashing,
                                                   self._timer_tl_cb)
                
            elif self._state == TrafficLightsState.GREEN_FLASHING:
                self._counter_blink += 1
                if self._counter_blink >= (2*self._param_green_flashing_repetitions):
                    self._state = TrafficLightsState.YELLOW_TO_RED
                    self._timer_tl = self.create_timer(self._param_duration_yellow,
                                    self._timer_tl_cb)
                    
            elif self._state == TrafficLightsState.YELLOW_TO_RED:
                self._state = TrafficLightsState.RED
                self._counter_blink = 0
                self._timer_tl.destroy()
                self._timer_tl = self.create_timer(self._param_duration_red,
                                                   self._timer_tl_cb)
                
        elif self._param_mode == TrafficLightsMode.OFF:
            self._state = TrafficLightsState.OFF

        elif self._param_mode == TrafficLightsMode.OFF_FLASHING:
            self._state = TrafficLightsState.YELLOW_FLASHING
            self._counter_blink = 0
            self._timer_tl.destroy()
            self._timer_tl = self.create_timer(self._param_duration_yellow_flashing,
                                                self._timer_tl_cb)                


    def _param_update_cb(self, paras: list[Parameter]) -> None:
        for p in paras:
            if p.name == "duration_green":
                self._param_duration_green = self.get_parameter("duration_green").get_parameter_value().double_value
            elif p.name == "duration_red":
                self._param_duration_red = self.get_parameter("duration_red").get_parameter_value().double_value
            elif p.name == "duration_yellow":
                self._param_duration_yellow = self.get_parameter("duration_yellow").get_parameter_value().double_value
            
            elif p.name == "green_flashing_repetitions":
                self._param_green_flashing_repetitions = self.get_parameter("green_flashing_repetitions").get_parameter_value().integer_value
            elif p.name == "duration_green_flashing":
                self._param_duration_green_flashing = self.get_parameter("duration_green_flashing").get_parameter_value().double_value

            elif p.name == "duration_yellow_flashing":
                self._param_duration_yellow_flashing = self.get_parameter("duration_yellow_flashing").get_parameter_value().double_value

            elif p.name == "mode":
                self._param_mode = TrafficLightsMode[self.get_parameter("mode").get_parameter_value().string_value]

    def destroy_node(self):
        return super().destroy_node()

def main():
    node = None
    try:
        rclpy.init()
        try:
            node = TrafficLightsServiceNode("traffic_lights_service")
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