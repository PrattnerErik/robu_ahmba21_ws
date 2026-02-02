from asyncio import Future
from rclpy.node import Node
import rclpy
import time
from turn_signal_interfaces.srv import TurnSignal

#Service-Call in der CLI
#Füge hier deinen Kommentar ein: 1P
#ros2 service call <service_name> <service_type> <arguments>
#ros2 service call /turn_signal_service turn_signal_interfaces/srv/TurnSignal '{cmd: "left", repetitions: 10}'

class TurnSignalClientNode(Node):
    def __init__(self, node_name: str): #2P
        super().__init__(node_name)

        self._turn_signal_client = self.create_client(TurnSignal, "/turn_signal")

        while not self._turn_signal_client.wait_for_service(1.0):
            self.get_logger().info("warte auf service...")
    
    def send_turn_signal_request(self, side:str="left", 
                                 repetitions:int=10) -> Future: #4P
        
        request = TurnSignal.Request()
        request.cmd = side
        request.repetitions = repetitions

        future = self._turn_signal_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()

        self.get_logger().info(response.success)
        

    def destroy_node(self):
        return super().destroy_node()

def main():
    node = None
    try:
        rclpy.init()
        try:
            node = TurnSignalClientNode("turn_signal_client")
            while True:
                node.send_turn_signal_request("left", 10)
                time.sleep(5)
                node.send_turn_signal_request("right", 10)
                time.sleep(5)
                node.send_turn_signal_request("warn", 10)
                time.sleep(5)
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

