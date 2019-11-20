#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Bool
from ur_control_wrapper.srv import SetPose
from ur_control_wrapper.srv import GetPose

class Demo:
    def __init__(self):
        self.free_drive_pub = rospy.Publisher("/ur_control_wrapper/enable_freedrive", Bool, queue_size=10)
        self.gripper_pub = rospy.Publisher("/ur_control_wrapper/gripper", Bool, queue_size=10)
        self.connect_pub = rospy.Publisher("/ur_control_wrapper/connect", Bool, queue_size=10)
    
    def move_arm(self, direction):
        rospy.wait_for_service("/ur_control_wrapper/get_pose")
        get_current_pose = rospy.ServiceProxy("/ur_control_wrapper/get_pose", GetPose)
        current_pose = None
        try:
            current_pose = get_current_pose()
        except rospy.ServiceException as exc:
            print "Service did not process request: " + str(exc)
        
        rospy.wait_for_service("/ur_control_wrapper/set_pose")
        set_current_pose = rospy.ServiceProxy("/ur_control_wrapper/set_pose", SetPose)
        try:
            if direction == "x+":
                current_pose.position.x += 0.05
            elif direction == "x-":
                current_pose.posiiton.x -= 0.05
            elif direction == "y+":
                current_pose.position.y += 0.05
            elif direction == "y-":
                current_pose.position.y -= 0.05
            elif direction == "z+":
                current_pose.position.z += 0.05
            elif direction == "z-":
                current_pose.position.z -= 0.05             
            pose, is_reached = set_current_pose(current_pose)
        except rospy.ServiceException as exc:
            print "Service did not process request: " + str(exc)
    
    def run(self):
        while not rospy.is_shutdown():
            command_input = raw_input("Freedrive: fs(start);\nfe-end: Gripper: go(open); gc(close);\nConnect: c(connect);\nMove arm: x+(x direction move up 5 cm); x-; y+; y-; z+; z-: \n")
            if command_input == "fs":
                self.free_drive_pub(True)
            elif command_input == "fe":
                self.free_drive_pub(False)
            elif command_input == "go":
                self.gripper_pub(True)
            elif command_input == "gc":
                self.gripper_pub(False)
            elif command_input == "c":
                self.connect_pub(True)
            else: # move arm
                direction = command_input
                self.move_arm(direction)

if __name__ == '__main__':
    try:
        rospy.init_node('ur_control_wrapper_demo_mode', anonymous=True)

        demo = Demo()

        demo.run()
    except rospy.ROSInterruptException:
        pass