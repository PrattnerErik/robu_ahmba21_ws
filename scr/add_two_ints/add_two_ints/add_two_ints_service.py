from rclpy.node import Node
import rclpy
from add_two_ints_interfaces.srv import AddTwoInts


class AddTwoIntsService(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        self._srv_add_two_ints = self.create_service(AddTwoInts, "add_two_ints", self._srv_add_two_ints_cb)

    def destroy_node(self):
        return super().destroy_node()

    def _srv_add_two_ints_cb(self, request:AddTwoInts.Request, response:AddTwoInts.Response) -> AddTwoInts.Response:
        response.sum = request.a + request.b

        return response


def main():
    node = None
    try:
        rclpy.init()
        try:
            node = AddTwoIntsService("add_two_ints_service")
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