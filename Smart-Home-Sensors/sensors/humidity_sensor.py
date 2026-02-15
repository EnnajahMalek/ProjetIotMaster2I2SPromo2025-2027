import random
from .virtual_sensor import VirtualSensor


class HumiditySensor(VirtualSensor):

    def __init__(self):
        super().__init__(
            initial_value=50,
            min_value=0,
            max_value=100,
            inertia=0.02,
            noise_level=0.2
        )

    def read_value(self):

        # humidité dépend légèrement de température ambiante fictive
        target = 60 + random.uniform(-5, 5)

        return self.update(target)

humidity = HumiditySensor()
