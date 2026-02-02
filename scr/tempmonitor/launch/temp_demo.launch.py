# snippid:
# ros_launch_file_node

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os

def generate_launch_description():

    # ----- parameter -----

    #temp sensor
    arg_mean = DeclareLaunchArgument('mean',
                                    default_value='25.0',
                                    description='Durchschnittliche Temperatur')
    arg_amplitude = DeclareLaunchArgument('amplitude',
                                    default_value='5.0',
                                    description='Amplitude Temperatur')
    arg_hz = DeclareLaunchArgument('hz',
                                    default_value='1.0',
                                    description='Messfrequenz')
    #temp monitor
    arg_threshold = DeclareLaunchArgument('threshold',
                                    default_value='27.5',
                                    description='Schwelltemperatur, bei der Alarm gegeben wird')

    # ----- nodes -----

    # code snippit: ros_launch_node_param
    node_temp_sensor = Node(
        package='tempmonitor',
        executable='temp_sensor',
        name='temp_sensor_node',
        parameters=[{
            'mean': LaunchConfiguration('mean'),
            'amplitude': LaunchConfiguration('amplitude'),
            'hz': LaunchConfiguration('hz'),           
        }],
        output='screen',
    )
    node_temp_monitor = Node(
        package='tempmonitor',
        executable='temp_monitor',
        name='temp_monitor_node',
        parameters=[{
            'threshold': LaunchConfiguration('threshold')
        }],
        output='screen',
    )

    ld = LaunchDescription()

    ld.add_action(arg_mean)
    ld.add_action(arg_amplitude)
    ld.add_action(arg_hz)
    ld.add_action(arg_threshold)

    ld.add_action(node_temp_sensor)
    ld.add_action(node_temp_monitor)

    return ld