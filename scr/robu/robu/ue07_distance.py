import rclpy        # importiert ros2 framework
from geometry_msgs.msg import Twist # Datentyp von ros2
from rclpy.node import Node
from std_msgs.msg import Float32
from random import randrange


class DistanceSensorNode(Node):
    def __init__(self, node_name:str="distance_node"):
        super().__init__(node_name)
        
        self._pub_distance = self.create_publisher(Float32,"distance", 10)

        self.create_timer(0.1, self._measureAndPublishDistance)

    def _measureAndPublishDistance(self):
        distance_m = randrange(0,10000,1)/1000.0 #0 bis 10m in mm schritten
        self.get_logger().info(f"Distance: {distance_m: .2f}")

        distance_msg = Float32()
        distance_msg.data = distance_m

        self._pub_distance.publish(distance_msg)

class ObstacleAvoidense(Node):
    def __init__(self, node_name:str="obstacle_avoidense_node"):
        super().__init__(node_name)

        self._sub_distance = self.create_subscription(Float32, "/distance", self._subDistanceCallback, 10)
        self._pub_cmd_vel = self.create_publisher(Twist, "/cmd_vel", 10)

    def _subDistanceCallback(self, msg:Float32):
        distance_m = msg.data

        if distance_m < 2.0:
            self.get_logger().warn("WIII WUUU WIIII WUUU WIII WUUU")
            vel = Twist()
            vel.linear.x = 0.0  #m/s
            vel.angular.z = 0.0 #r/s

            self._pub_cmd_vel.publish(vel)

def main_distance_pub():

    try:
        rclpy.init()
        node = DistanceSensorNode()
        rclpy.spin(node)
        
    except KeyboardInterrupt:
        #STRG+C
        #sicher herunterfahren, aufräumen
        pass #dua nix
    finally:
        node.destroy_node()
        rclpy.shutdown()


def main_distance_sub():

    try:
        rclpy.init()
        node = ObstacleAvoidense()
        rclpy.spin(node)
        
    except KeyboardInterrupt:
        #STRG+C
        #sicher herunterfahren, aufräumen
        pass #dua nix
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main_distance_sub()