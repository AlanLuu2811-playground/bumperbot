from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import UnlessCondition, IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

import os

def generate_launch_description():
    use_slam_arg = DeclareLaunchArgument(
        "use_slam",
        default_value="false"
    )

    use_slam = LaunchConfiguration("use_slam")

    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('bumperbot_description'),
            'launch',
            'gazebo.launch.py'

        )
    )

    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('bumperbot_controller'),
            'launch',
            'controller.launch.py'
        ),
        launch_arguments = {
                'use_simple_controller': 'False',
                'use_python': 'False'
        }.items()
    )

    joystick = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('bumperbot_controller'),
            'launch',
            'joystick_teleop.launch.py'
        )
    )

    localization = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('bumperbot_localization'),
            "launch",
            "global_localization.launch.py"
        ),
        condition=UnlessCondition(use_slam)
    )

    slam = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory('bumperbot_mapping'),
            "launch",
            "slam.launch.py"
        ),
        condition=IfCondition(use_slam)
    )

    safety_stop = Node(
        package="bumperbot_utils",
        executable="safety_stop",
        output="screen"
    )

    rviz = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", os.path.join(
            get_package_share_directory("nav2_bringup"),
            "rviz",
            "nav2_default_view.rviz"
        )],
        output="screen",
        parameters=[{"use_sim_time": True}]
    )

    return LaunchDescription([
        use_slam_arg,
        gazebo,
        controller,
        joystick,
        #safety_stop,
        localization,
        slam,
        rviz
    ])
