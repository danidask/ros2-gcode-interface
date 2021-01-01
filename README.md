

# TEST

ros2 run gcode_interface gcode_interface
ros2 topic pub /gcode_pose geometry_msgs/Point  "{x: 0.0, y: 0.0, z: 0.0}"
