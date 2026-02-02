from rclpy.node import Node
import rclpy
from turn_signal_interfaces.srv import TurnSignal

class TurnSignalServiceNode(Node):    
    def __init__(self, node_name: str): #4P
        super().__init__(node_name)

        self._srv_turn_signal = self.create_service(TurnSignal, "turn_signal", self._srv_turn_signal_callback)

        self._blinke_rechts = [False, False, False]
        self._blinke_links = [False, False, False]

        self.declare_parameter("turn_signal_interval", 0.5)
        self._param_turn_signal_interval = self.get_parameter("turn_signal_interval").get_parameter_value().double_value

        self._repetitions = 0
        self._cmd = ""
        self._counter = 0

    
    def _srv_turn_signal_callback(self, 
                                  request:TurnSignal.Request, 
                                  response:TurnSignal.Response) -> TurnSignal.Response: #4P
        self._cmd = request.cmd
        self._repetitions = request.repetitions

        if not self._cmd == "left" and not self._cmd == "right" and not self._cmd == "warn":
            self.get_logger().warn("cmd muss right, left oder warn sein")
        else:
            self._turn_signal_timer = self.create_timer(self._param_turn_signal_interval, self._timer_turn_signal_callback)
        
        return response



    def _timer_turn_signal_callback(self):  #3P+2P+2EP
        
        if self._counter < self._repetitions:
            if self._cmd == "right":
                if self._counter%2:
                    self._blinke_rechts = [True , True, True]
                else:
                    self._blinke_rechts = [False, False, False]
            if self._cmd == "left":
                if self._counter%2:
                    self._blinke_links = [True , True, True]
                else:
                    self._blinke_links = [False, False, False]
            if self._cmd == "warn":
                if self._counter%2:
                    self._blinke_links = [True , True, True]
                    self._blinke_rechts = [True , True, True]
                else:
                    self._blinke_links = [False, False, False]
                    self._blinke_rechts = [False, False, False]
            if self._cmd == "left_modern":
                if self._counter%3 == 0:
                    self._blinke_links = [True , False, False]
                elif self._counter%3 == 1:
                    self._blinke_links = [False, True, False]
                else:
                    self._blinke_links = [False, False, True]
            if self._cmd == "right_modern":
                if self._counter%3 == 0:
                    self._blinke_rechts = [False , False, True]
                elif self._counter%3 == 1:
                    self._blinke_rechts = [False, True, False]
                else:
                    self._blinke_rechts = [True, False, False]

            
            self._counter += 1
            left = ""
            for i in self._blinke_links:
                if i:
                    left += "<"
                else:
                    left += "0"
            right = ""
            for i in self._blinke_rechts:
                if i:
                    right += "<"
                else:
                    right += "0"
            signal = left + "    " + right
            self.get_logger().info(signal)
            
        else:
            self._turn_signal_timer.destroy()
        
    
    def destroy_node(self):
        return super().destroy_node()

def main():
    node = None
    try:
        rclpy.init()
        try:
            node = TurnSignalServiceNode("turn_signal_service")
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

