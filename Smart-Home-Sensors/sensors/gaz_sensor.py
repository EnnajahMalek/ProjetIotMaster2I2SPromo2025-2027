import random
from .virtual_sensor import VirtualSensor


class GasSensor(VirtualSensor):

    def __init__(self):
        super().__init__(
            initial_value=100,
            min_value=0,
            max_value=1000,
            inertia=0.1,
            noise_level=5
        )

        self.leak = False

    def trigger_leak(self, state: bool):
        self.leak = state

    def read_value(self):

        if self.leak:
            target = 800
        else:
            target = 100

        return self.update(target)

gaz = GasSensor()