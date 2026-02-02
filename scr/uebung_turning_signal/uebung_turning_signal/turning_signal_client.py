from rclpy.node import Node
import rclpy
from uebung_turning_signal_interfaces.srv import Signal

class TurningSignalClient(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        self._cli_turning_signal = self.create_client(Signal, "turning_signal_service")

        while not self._cli_turning_signal.wait_for_service(1):
            self.get_logger().warn("waiting for service")

    def send_turn_signal_request(self, cmd:str, repetitions:int=8):
        request = Signal.Request()
        request.cmd = cmd
        request.repetitions = repetitions

        future = self._cli_turning_signal.call_async(request)
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
            node = TurningSignalClient("truning_signal_client")
            node.send_turn_signal_request("r", 10)
        except Exception as e:
            print(f"Fehler beim Erstellen des Nodes: {e}")
            return

        rclpy.spin_once(node)

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