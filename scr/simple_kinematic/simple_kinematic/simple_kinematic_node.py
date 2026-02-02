from rclpy.node import Node
import rclpy
from turtlesim.msg import Pose

class SimpleKinematicNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        self._sub_turtle1_pose = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self._sub_turtle1_pose_cb,
            10
        )
        self._sub_turtle2_pose = self.create_subscription(
            Pose,
            '/turtle2/pose',
            self._sub_turtle2_pose_cb,
            10
        )
        self._turtle1_pose = Pose()
        self._turtle2_pose = Pose()

    def destroy_node(self):
        return super().destroy_node()
    
    def _sub_turtle1_pose_cb(self, msg:Pose):
        self._turtle1_pose = msg
        #self.get_logger().info(f"Pose turtle1: {msg.x:.2f}, {msg.y:.2f}, {msg.theta:.2f}")

    def _sub_turtle2_pose_cb(self, msg:Pose):
        self._turtle2_pose = msg
        #self.get_logger().info(f"Pose turtle2: {msg.x:.2f}, {msg.y:.2f}, {msg.theta:.2f}")
        self._distance()
    
    def _distance(self):
        from math import pi, cos, sin
        t_x = self._turtle2_pose.x - self._turtle1_pose.x
        t_y = self._turtle2_pose.y - self._turtle1_pose.y

        d_theta = self._turtle2_pose.theta - self._turtle1_pose.theta #radiant
        d_theta_deg = d_theta * 180/pi # umgerechnet in grad (degries)

        r11 = cos(d_theta)
        r12 =-sin(d_theta)
        r21 = sin(d_theta)
        r22 = cos(d_theta)

        dist = (t_x ** 2 + t_y ** 2) ** .5

        self.get_logger().info(f'Entfernung: {dist: .2f}')
        self.get_logger().info(f'Rotations-Matrix:')
        self.get_logger().info(f'{r11: 5.2f}, {r12: 5.2f}')
        self.get_logger().info(f'{r21: 5.2f}, {r22: 5.2f}')
        self.get_logger().info(f'delta-theta in grad: {d_theta_deg: .2f}')




def main():
    node = None
    try:
        rclpy.init()
        try:
            node = SimpleKinematicNode("simple_kinematic")
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