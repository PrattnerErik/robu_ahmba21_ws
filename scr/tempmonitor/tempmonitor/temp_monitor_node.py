from rclpy.node import Node
import rclpy
from std_msgs.msg import Float32, String
from rcl_interfaces.msg import ParameterDescriptor, Parameter, SetParametersResult

class TempMonitorNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        #create subscriber
        self._sub_temp_sensor = self.create_subscription(Float32, "temperature", self._sub_temp_sensor_cb, 10)

        #create publisher
        self._pub_temp_alarm = self.create_publisher(String, "temperature_alarm", 10)

        #parameter
        self.declare_parameter("threshold", .5, ParameterDescriptor(description="Temperaturschwelle, an welcher alarm gegeben wird"))
        self._threshold = self.get_parameter("threshold").get_parameter_value().double_value
        self.add_on_set_parameters_callback(self._on_parameter_set_callback)
    
    def _on_parameter_set_callback(self, parameter:list[Parameter]):
        for p in parameter:
            if p.name == "threshold":
                self._threshold = float(p.value)
        return SetParametersResult(successful=True)
    
    def _sub_temp_sensor_cb(self, msg:Float32):
        temp = msg.data

        if temp > self._threshold:
            msg = String()
            msg.data = f'WARNING: temperatur über threshold: {temp:.2f} °C'
            self._pub_temp_alarm.publish(msg)
            self.get_logger().warning(msg.data)
    
    def _publish_warning(self, temp):
        # create and publish message
        msg = String()
        msg.data = f'WARNING: temperatur über threshold: {temp:.2f} °C'
        self.publisher_.publish(msg)

        # log to console
        self.get_logger().warning(f'WARNING: temperatur über threshold: {temp:.2f} °C')




    def destroy_node(self):
        return super().destroy_node()

def main():
    node = None
    try:
        rclpy.init()
        try:
            node = TempMonitorNode("temp_monitor_noe")
        except Exception as e:
            print(f"Fehler beim Erstellen des Nodes: {e}")
            return

        rclpy.spin(node)

    except KeyboardInterrupt:
        print("heeeeeeEEEEEEEE STRG+C ... is net cool... ok??")

    finally:
        if node is not None:
            if rclpy.ok():
                node.get_logger().info(f"Node {node.get_name()} wird beendet!")
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()