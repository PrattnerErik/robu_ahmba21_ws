from rclpy.node import Node
import rclpy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist, TwistStamped

class obstacleAvoidenceNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        #Subscriber - LIDAR daten empfangen
        self._sub_scan = self.create_subscription(LaserScan, "scan", self._sub_scan__sb, 10)

        #Publisher - geschw. senden
        self._pub_cmd_vel = self.create_publisher(TwistStamped, "cmd_vel", 10)

    def _sub_scan__sb(self, msg:LaserScan):

        dist_min = min(msg.ranges)
        if dist_min < .5:
            self.get_logger().warn(f"Minimale Distanz wurde Unterschritten: Aktuelle Distanz: {dist_min: .2f}")

            vel = TwistStamped()
            vel.twist.linear.x = 0.0
            vel.twist.linear.y = 0.0
            vel.twist.linear.z = 0.0
            vel.twist.angular.x = 0.0
            vel.twist.angular.y = 0.0
            vel.twist.angular.z = 0.0

            self._pub_cmd_vel.publish(vel)
                    

    def destroy_node(self):
        return super().destroy_node()





def main():
    node = None
    try:
        rclpy.init()
        try:
            node = obstacleAvoidenceNode("obstacle_avoidence")
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