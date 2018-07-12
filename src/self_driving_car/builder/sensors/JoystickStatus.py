from morse.builder.creator import SensorCreator
from morse.builder.blenderobjects import Sphere

class Joystickstatus(SensorCreator):
    _classpath = "self_driving_car.sensors.JoystickStatus.Joystickstatus"
    _blendname = "JoystickStatus"

    def __init__(self, name=None):
        SensorCreator.__init__(self, name)

