from rclpy.node import Node
import rclpy
from add_two_ints_interfaces.srv import AddTwoInts

class AddTwoIntsClient(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        self._cli_add_two_ints = self.create_client(AddTwoInts, "/add_two_ints")
        
        while not self._cli_add_two_ints.wait_for_service(1.0):
            self.get_logger().info("service no net do chilllllll amol")

    def destroy_node(self):
        return super().destroy_node()

    def send_request(self, a, b):
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        self.get_logger().info(f'add {a} and {b}')
        future = self._cli_add_two_ints.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()

        #response:AddTwoInts.Response = self._cli_add_two_ints.call(request, 5.0)
        self.get_logger().info(f"{a} + {b} = {response.sum}")

def main():
    node = None
    try:
        rclpy.init()
        try:
            node = AddTwoIntsClient("add_two_ints_client")
            node.send_request(43, 24)
        except Exception as e:
            print(f"Fehler beim Erstellen des Nodes: {e}")
            return

        #rclpy.spin(node)
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