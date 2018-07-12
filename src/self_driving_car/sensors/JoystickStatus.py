import logging; logger = logging.getLogger("morse." + __name__)

import morse.core.sensor

from morse.core.services import service, async_service
from morse.core import status
from morse.core import blenderapi
from morse.helpers.components import add_data, add_property

class Joystickstatus(morse.core.sensor.Sensor):
    """Write here the general documentation of your sensor.
    It will appear in the generated online documentation.
    """
    _name = "Joystickstatus"
    _short_desc = "Returns position of joystick."

    # define here the data fields exported by your sensor
    # format is: field name, default initial value, type, description
    add_data('horizontal_axis', 0.0, 'float', 'Horizontal posisiton joystick.')

    def __init__(self, obj, parent=None):
        logger.info("%s initialization" % obj.name)
        # Call the constructor of the parent class
        morse.core.sensor.Sensor.__init__(self, obj, parent)

        # Do here sensor specific initializations
        joysticks = blenderapi.joysticks()
        
        if joysticks.count(None) == len(joysticks):
            logger.error("No Joystick detected")
        else:
            logger.info("Found Joystick: " + repr(joysticks) )

        logger.info('Component initialized')

    @service
    def get_horizontal_axis(self):
        """ This is a sample (blocking) service (use 'async_service' decorator
        for non-blocking ones).

        Simply returns the value of the internal counter.

        You can access it as a RPC service from clients.
        """
        logger.info("%s is in position: %sm" % (self.name, self.local_data['horizontal_axis']))

        return self.local_data['horizontal_axis']

    def default_action(self):
        """ Main loop of the sensor.

        Implements the component behaviour
        """

        # implement here the behaviour of your sensor
        joysticks = blenderapi.joysticks()       
        joystick_sensor = joysticks[0]
        rz = joystick_sensor.axisValues[0] 
        self.local_data['horizontal_axis'] = rz


