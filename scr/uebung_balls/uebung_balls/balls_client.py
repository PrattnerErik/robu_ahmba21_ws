from rclpy.node import Node
import rclpy
from uebung_balls_interfaces.srv import Balls

class BallsClientNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        self._balls_client = self.create_client(Balls, "/balls_service")

        while not self._balls_client.wait_for_service(1):
            self.get_logger().info("waiting for the ball fondler")

    def destroy_node(self):
        return super().destroy_node()
    
    def use_balls(self):
        request = Balls.Request()
        request.msg = "in your jaw"

        self.get_logger().info("asking the ball mashine")

        future = self._balls_client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        response = future.result()

        self.get_logger().info(response.msg)



def main():
    node = None
    try:
        rclpy.init()
        try:
            node = BallsClientNode("balls_client_node")
            node.use_balls()
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