from rclpy.node import Node
import rclpy
from uebung_turning_signal_interfaces.srv import Signal


class TurningSignalService(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        self._repetitions = 0
        self._cmd = ""
        self._lights_r = [False, False, False]
        self._lights_l = [False, False, False]
        self._counter = 0

        self._ser_turnuing_signal = self.create_service(Signal, "turning_signal_service", self._service_cb)
        
        self.declare_parameter("interval", 0.5)
        self._interval = self.get_parameter("interval").get_parameter_value().double_value

    def _service_cb(self, request:Signal.Request , response:Signal.Response) -> Signal.Response:

        self._cmd = request.cmd
        self._repetitions = request.repetitions

        if self._cmd == "r" or self._cmd == "l" or self._cmd == "wa":
            response.success = True
            self._timer = self.create_timer(self._interval, self._timer_cb)
        else:
            response.success = False

        return response
    
    def _timer_cb(self):
        if self._counter < self._repetitions:
            self._counter += 1

            if self._cmd == "w":
                if self._counter %2:
                    self._lights_r = [False, False, False]
                    self._lights_l = [False, False, False]
                else:
                    self._lights_r = [True, True, True]
                    self._lights_l = [True, True, True]
            
            elif self._cmd == "r":
                if self._counter %3 == 0:
                    self._lights_r = [True, False, False]
                elif self._counter %3 == 1:
                    self._lights_r = [False, True, False]
                else:
                    self._lights_r = [False, False, True]

            elif self._cmd == "l":
                if self._counter %3 == 0:
                    self._lights_l = [True, False, False]
                elif self._counter %3 == 1:
                    self._lights_l = [False, True, False]
                else:
                    self._lights_l = [False, False, True]

            signal = ""
            for i in self._lights_l:
                if i:
                    signal += "<"
                else:
                    signal += "o"
            signal += "                 "
            for i in self._lights_r:
                if i:
                    signal += ">"
                else:
                    signal += "o"
            self.get_logger().info(signal)

        else:
            self._counter = 0
            self.destroy_timer(self._timer)

    def destroy_node(self):
        return super().destroy_node()

def main():
    node = None
    try:
        rclpy.init()
        try:
            node = TurningSignalService("turning_signal_service")
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