from pyniryo import *


robot = NiryoRobot("127.0.0.1")


robot.calibrate_auto()


robot.set_brightness(1)
robot.set_contrast(1)


# - Constants
workspace_name = "gazebo_1"  # Robot's Workspace Name


# The pose from where the image processing happens
observation_pose = PoseObject(
    x=0.16, y=0.0, z=0.35,
   roll=0.0, pitch=1.57, yaw=0.0,
)


# Place pose
place_pose = PoseObject(
   x=0.0, y=-0.2, z=0.12,
   roll=0.0, pitch=1.57, yaw=-1.57
)


# - Initialization


# Connect to robot
# Calibrate robot if the robot needs calibration
robot.update_tool()


# Initializing variables
offset_size = 0.05
max_catch_count = 4


# Loop until enough objects have been caught
catch_count = 0
while catch_count < max_catch_count:
   # Moving to observation pose
   robot.move_pose(observation_pose)


   # Trying to get object via Vision Pick
   obj_found, shape, color = robot.vision_pick(workspace_name)
   if not obj_found:
       robot.wait(0.1)
       continue


   # Calculate place pose and going to place the object
   next_place_pose = place_pose.copy_with_offsets(x_offset=catch_count * offset_size)
   robot.place_from_pose(next_place_pose)


   catch_count += 1


robot.go_to_sleep()
robot.close_connection()

