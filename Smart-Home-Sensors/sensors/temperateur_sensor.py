import math
import time
from .virtual_sensor import VirtualSensor

class TemperatureSensor(VirtualSensor):

    def __init__(self):
        super().__init__(
            initial_value=22.0,
            min_value=0,
            max_value=50,
            inertia=0.03,
            noise_level=0.05
        )

        self.ac_on = False
        self.start_time = time.time()

    def toggle_ac(self, state: bool):
        self.ac_on = state

    def _outside_temperature(self):
        hours = (time.time() - self.start_time) / 3600
        return 30 + 5 * math.sin(2 * math.pi * hours / 24)

    def read_value(self):

        outside = self._outside_temperature()

        if self.ac_on:
            outside -= 5  

        return self.update(outside)



