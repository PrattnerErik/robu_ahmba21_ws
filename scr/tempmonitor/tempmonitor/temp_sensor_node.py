# snippid:
# ros2_main_class

from rcl_interfaces.msg import ParameterDescriptor, Parameter, SetParametersResult
from rclpy.node import Node
import rclpy
from std_msgs.msg import Float32
import time
import random

class TempSensorNode(Node):
    def __init__(self, node_name: str):
        super().__init__(node_name)

        #publisher für temperatur
        self._pub_temp = self.create_publisher(Float32, "temperature", 10)

        #param mean
        self.declare_parameter("mean", .5, ParameterDescriptor(description="durchschnittliche temperatur die wiedergegeben wird"))
        self._mean = self.get_parameter("mean").get_parameter_value().double_value
        #param amplitude
        self.declare_parameter("amplitude", .5, ParameterDescriptor(description="amplitude temperatur die wiedergegeben wird"))
        self._amplitude = self.get_parameter("amplitude").get_parameter_value().double_value
        #param hz
        self.declare_parameter("hz", .5, ParameterDescriptor(description="Freqzuenz in welcher temperatur wiedergegeben wird"))
        self._hz = self.get_parameter("hz").get_parameter_value().double_value
        # add callback to parameters
        self.add_on_set_parameters_callback(self._on_parameter_set_callback)


        #run timer - bis node gestoppt wird
        self._start_timer()

    def _on_parameter_set_callback(self, parameter:list[Parameter]):
        for p in parameter:
            if p.name == "mean":
                self._mean = float(p.value)
            if p.name == "amplitude":
                self._amplitude = float(p.value)
            if p.name == "hz":
                self._hz = float(p.value)
        return SetParametersResult(successful=True)

    def destroy_node(self):
        return super().destroy_node()
    
    def _start_timer(self):
        interval = 1.0 / self._hz

        while True:
            tick_start = time.perf_counter()

            self._publish_temp()
            
            elapsed = time.perf_counter() - tick_start
            sleep_time = interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    def _publish_temp(self):
        # generate random temperature
        temp = self._create_imaginary_temp()

        # create and publish message
        msg = Float32()
        msg.data = temp
        self._pub_temp.publish(msg)

        # log to console
        self.get_logger().info(f'Published temperature: {temp:.2f} °C')

    def _create_imaginary_temp(self):
        return random.uniform(self._mean - self._amplitude, self._mean + self._amplitude)


def main():
    node = None
    try:
        rclpy.init()
        try:
            node = TempSensorNode("temp_sensor_node")
        except Exception as e:
            print(f"Fehler beim Erstellen des Nodes: {e}")
            return

        rclpy.spin(node)

    except KeyboardInterrupt:
        print("schtrng CCCC")

    finally:
        if node is not None:
            if rclpy.ok():
                node.get_logger().info(f"Node {node.get_name()} wird beendet!")
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()       

