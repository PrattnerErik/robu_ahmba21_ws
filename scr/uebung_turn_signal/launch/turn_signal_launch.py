from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    param_turn_signal_interval = DeclareLaunchArgument('turn_signal_interval', default_value='0.5', description='Interval vom blinken')

    turn_signal_service = Node(
        package='turn_signal',
        executable='turn_signal_service',
        name='turn_signal_service',
        parameters=[{
            'turn_signal_interval': LaunchConfiguration('turn_signal_interval')
        }]
    )
    turn_signal_client = Node(
        package='turn_signal',
        executable='turn_signal_client',
        name='turn_signal_client',
        parameters=[{
        }]
    )

    ld = LaunchDescription()
    ld.add_action(param_turn_signal_interval)
    ld.add_action(turn_signal_service)
    ld.add_action(turn_signal_client)
    return ld


# ros2 launch turn_signal turn_signal_launch.py 
#[INFO] [launch]: All log files can be found below /home/robu/.ros/log/2025-12-01-09-24-10-686048-robu-desktop-16833
#[INFO] [launch]: Default logging verbosity is set to INFO
#[INFO] [turn_signal_service-1]: process started with pid [16836]
#[INFO] [turn_signal_client-2]: process started with pid [16837]
#[turn_signal_client-2] [INFO] [1764581051.640582281] [turn_signal_client]: Node turn_signal_client wird beendet!
#[INFO] [turn_signal_client-2]: process has finished cleanly [pid 16837]
#[turn_signal_service-1] [INFO] [1764581052.149494455] [turn_signal_service]: 000    000
#[turn_signal_service-1] [INFO] [1764581052.624870515] [turn_signal_service]: <<<    000
#[turn_signal_service-1] [INFO] [1764581053.113999717] [turn_signal_service]: 000    000
#[turn_signal_service-1] [INFO] [1764581053.610553345] [turn_signal_service]: <<<    000
#[turn_signal_service-1] [INFO] [1764581054.110952779] [turn_signal_service]: 000    000
#[turn_signal_service-1] [INFO] [1764581054.613081320] [turn_signal_service]: <<<    000
#[turn_signal_service-1] [INFO] [1764581055.115871356] [turn_signal_service]: 000    000
#[turn_signal_service-1] [INFO] [1764581055.613358577] [turn_signal_service]: <<<    000
#[turn_signal_service-1] [INFO] [1764581056.111129080] [turn_signal_service]: 000    000
#[turn_signal_service-1] [INFO] [1764581056.611819198] [turn_signal_service]: <<<    000
