from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():


    add_two_ints_service = Node(
        package='add_two_ints',
        executable='add_two_ints_service',
        name='add_two_ints_service',
        output='screen',
        parameters=[]
    )
    add_two_ints_client = Node(
        package='add_two_ints',
        executable='add_two_ints_client',
        name='add_two_ints_client',
        output='screen',
        parameters=[]
    )

    ld = LaunchDescription()
    ld.add_action(add_two_ints_service)
    ld.add_action(add_two_ints_client)
    return ld