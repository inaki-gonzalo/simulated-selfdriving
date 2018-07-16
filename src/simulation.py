from morse.builder import *
from self_driving_car.builder.sensors import Joystickstatus

# Land robot
atrv = ATRV()
atrv.translate(y=1.5)
atrv.rotate(0,0,0.5)

motion = MotionVW()
atrv.append(motion)

videocamera = VideoCamera("POV_robot")
videocamera.translate(0,0, 4)
videocamera.rotate(0, -0.5, 0)
atrv.append(videocamera)

videocamera2 = VideoCamera("POV_person")
videocamera2.translate(0,0, 4)
videocamera2.rotate(0, -0.5, 0)
atrv.append(videocamera2)

#Add Joystick Sensor
joy=Joystickstatus()
atrv.append(joy)

#Add interfaces for sensors
motion.add_interface('socket')
videocamera.add_interface('socket')
joy.add_interface('socket')

#Setup Scene
env = Environment('my_racetrack.blend')
env.set_camera_location([5, -5, 6])
env.set_camera_rotation([1.0470, 0, 0.7854])
