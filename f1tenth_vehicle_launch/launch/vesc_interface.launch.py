from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    f1tenth_vehicle_launch_dir = FindPackageShare('f1tenth_vehicle_launch')

    # Default files
    vesc_driver_config_file = PathJoinSubstitution([f1tenth_vehicle_launch_dir, 'config', 'vesc_driver.param.yaml'])
    vesc_interface_config_file = PathJoinSubstitution([
        f1tenth_vehicle_launch_dir, 'config', 'vesc_interface.param.yaml'])

    # Create launch configuration variables
    vesc_interface_config = LaunchConfiguration('vesc_interface_config')
    vesc_driver_config = LaunchConfiguration('vesc_driver_config')

    # Declare Launch Arguments
    vesc_interface_la = DeclareLaunchArgument(
            'vesc_interface_config',
            default_value=vesc_interface_config_file,
            description='Descriptions for vesc configs')
    vesc_driver_la = DeclareLaunchArgument(
            'vesc_driver_config',
            default_value=vesc_driver_config_file,
            description='Descriptions for vesc configs')

    ld = LaunchDescription([vesc_interface_la, vesc_driver_la])

    # Setup Node
    container = ComposableNodeContainer(
        name='vesc_interface_container',
        namespace='',
        package='rclcpp_components',
        executable='component_container',
        composable_node_descriptions=[
                ComposableNode(
                    package='vesc_interface',
                    # remappings=[("/sensors/imu", "/imu")],
                    plugin='vesc_interface::VescInterfaceNode',
                    name='vesc_interface_node',
                    parameters=[
                        vesc_interface_config,
                        vesc_driver_config
                    ],
                ),
        ],
        output='screen',
        arguments=['--ros-args', '--log-level', 'info', '--enable-stdout-logs']
    )

    # add nodes to the launch description
    ld.add_action(container)
    return ld
