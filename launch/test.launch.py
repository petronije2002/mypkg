import os

from ament_index_python.packages import get_package_share_directory
from launch.actions import TimerAction

from launch.actions import DeclareLaunchArgument

from launch import LaunchDescription
from launch.actions import  IncludeLaunchDescription,ExecuteProcess,RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.event_handlers import OnProcessExit

from launch_ros.actions import Node

import xacro


def generate_launch_description():



    lib = "/opt/ros/foxy/lib"
    package_dir=get_package_share_directory('mypkg')
    world_file = os.path.join(package_dir,'worlds/test.world')
    
    default_rviz_config_path = os.path.join(package_dir, 'rviz/rviz_config.rviz')
    
    
   

   
   
    # gazebo = IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
    #                  launch_arguments={'use_sim_time': 'true' }.items()
    #          )


    
    

    xacro_robot_pkg_path = os.path.join(
        get_package_share_directory('mypkg'))

    xacro_file = os.path.join(xacro_robot_pkg_path,
                                'urdf',
                                'test.xacro.urdf')
    

    # print("WORLD", world_file)
    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    

    # doc = xacro.parse(open(xacro_file))
    # xacro.process_doc(doc)
    params = {'robot_description': doc.toxml(), 'use_sim_time': True}

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )


    follower= Node(package='mypkg',
    executable='follower',
    output='screen',
    parameters=[{'use_sim_time': True}])
    


    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
        launch_arguments={'use_sim_time': 'true', 
        'world': world_file}.items())
 
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                    arguments=['-topic', 'robot_description',
                                '-entity', 'my_bot'],
                    output='screen',

                    
                    )

    
    start_rviz_cmd = Node(
    package='rviz2',
    executable='rviz2',
    name='rviz2',
    output='screen',
     arguments=['-d', default_rviz_config_path],
     
     parameters=[params]
     
    )

   
   



    # load_joint_state_controller = ExecuteProcess(
    #     cmd=['ros2', 'control', 'load_controller', '--set-state', 'start',
    #          'joint_state_broadcaster'],
    #     output='screen',
        
    # )

    # load_diff_drive_base_controller = ExecuteProcess(
    #     cmd=['ros2', 'control', 'load_controller', '--set-state', 'start',
    #          'diff_drive_base_controller'],
    #     output='screen'
        
    # )


    

    node_static = Node(package = "tf2_ros", 
                       executable = "static_transform_publisher",
                       arguments = ["0", "0", "0", "0", "0", "0", "base_link", "world"],
                       parameters=[{'use_sim_time': 'true'}])

   


    return  LaunchDescription([

        node_robot_state_publisher,


        
        gazebo,
        spawn_entity,
        

      

        start_rviz_cmd,

        follower,

        node_static
        
       
        
       
    ])



