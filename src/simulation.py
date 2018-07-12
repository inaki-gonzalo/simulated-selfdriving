from morse.builder import *
from self_driving_car.builder.sensors import Joystickstatus

# Land robot
atrv = ATRV()
atrv.translate(y=13)

motion = MotionVW()
atrv.append(motion)

videocamera = VideoCamera("POV_robot")
videocamera.translate(0,0, 5)
videocamera.rotate(0, -0.4, 0)
atrv.append(videocamera)

videocamera2 = VideoCamera("POV_person")
videocamera2.translate(0,0, 5)
videocamera2.rotate(0, -0.4, 0)
atrv.append(videocamera2)

#Add Joystick Sensor
joy=Joystickstatus()
atrv.append(joy)

#Add interfaces for sensors
motion.add_interface('socket')
videocamera.add_interface('socket')
joy.add_interface('socket')

#Setup Scene
env = Environment('/home/tom/Downloads/trackTut18.blend')
env.set_camera_location([5, -5, 6])
env.set_camera_rotation([1.0470, 0, 0.7854])
