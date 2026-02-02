from rclpy.node import Node
import rclpy
from uebung_balls_interfaces.srv import Balls

class BallsServiceNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        self._balls_service = self.create_service(Balls, "balls_service", self._balls_service_cb)

        self._counter = 0



    def _balls_service_cb(self, request:Balls.Request, response:Balls.Response) -> Balls.Response:
        msg = request.msg
        self._counter = 0

        if msg == "fondle them":
            self.create_timer(1, self._fondle_timer_cb)
            response.msg = "balls are being fondled with"
        elif msg == "in your jaw":
            self.create_timer(1, self._jaw_timer_cb)
            response.msg = "balls are being put in your jaw"
        else:
            response.msg = "no balls?"
        
        return response

    def _fondle_timer_cb(self):
        if self._counter < 10:
            self.get_logger().info("can IIIIIIIII")
            self._counter +=1
        else:
            self.destroy_timer(self._fondle_timer_cb)

    def _jaw_timer_cb(self):

        if self._counter < 10:
            self.get_logger().info("fondle...")
            self._counter +=1
        else:
            self.destroy_timer(self._jaw_timer_cb)

        


    def destroy_node(self):
        return super().destroy_node()

def main():
    node = None
    try:
        rclpy.init()
        try:
            node = BallsServiceNode("balls_service_node")
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