from morse.builder import *
from self_driving_car.builder.sensors import Joystickstatus

# Land robot
atrv = ATRV()
atrv.translate(y=13)
videocamera = VideoCamera("POV_robot")
videocamera2 = VideoCamera("POV_person")

pose = Pose()
pose.translate(z = 0.75)
atrv.append(pose)

motion = MotionVW()
velocity = Velocity()
#motion = Waypoint()
atrv.append(motion)
atrv.append(velocity)




videocamera.translate(0,0, 5)
videocamera.rotate(0, -0.4, 0)
atrv.append(videocamera)

videocamera2.translate(0,0, 5)
videocamera2.rotate(0, -0.4, 0)
atrv.append(videocamera2)
# Add a keyboard controller to move the robot with arrow keys.
#keyboard = Keyboard()
#atrv.append(keyboard)
#keyboard.properties(ControlType = 'Position')

#joystick = Joystick()
#atrv.append(joystick)

joy=Joystickstatus()
atrv.append(joy)


# Scene configuration
#motion.add_service('socket')
motion.add_interface('socket')
pose.add_interface('socket')
videocamera.add_interface('socket')
velocity.add_interface('socket')
#joystick.add_interface('socket')
joy.add_interface('socket')

#env = Environment('indoors-1/indoor-1')
#env = Environment('outdoors')
env = Environment('/home/tom/Downloads/trackTut18.blend')
env.set_camera_location([5, -5, 6])
env.set_camera_rotation([1.0470, 0, 0.7854])
