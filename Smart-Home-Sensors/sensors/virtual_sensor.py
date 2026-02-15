import random

class VirtualSensor:

    def __init__(self,
                initial_value=0.0,
                min_value=None,
                max_value=None,
                inertia=0.05,
                noise_level=0.1):

        self.value = initial_value
        self.min_value = min_value
        self.max_value = max_value
        self.inertia = inertia
        self.noise_level = noise_level

    def _apply_limits(self):
        if self.min_value is not None:
            self.value = max(self.min_value, self.value)

        if self.max_value is not None:
            self.value = min(self.max_value, self.value)

    def _apply_noise(self):
        return random.gauss(0, self.noise_level)

    def update(self, target_value):
        """
        Modèle générique :
        value → converge progressivement vers target_value
        """

        delta = self.inertia * (target_value - self.value)
        noise = self._apply_noise()

        self.value += delta + noise
        self._apply_limits()

        return round(self.value, 2)
