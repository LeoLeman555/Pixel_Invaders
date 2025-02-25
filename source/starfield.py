import random
import pyxel as px


class StarField:
    def __init__(self):
        """Initialize the starfield."""
        self.stars_max = 7
        self.speed = 1.0  # Initial speed, will increase over time
        self.stars = [
            [
                random.randint(0, px.width),  # x
                random.randint(0, px.height),  # y
                random.uniform(2, 4),  # speed
            ]
            for _ in range(self.stars_max)
        ]

    def update(self):
        """Update the position of the stars and remove those that exit the screen."""
        self.speed = min(
            self.speed + 0.001, 3.0
        )  # Gradually increase speed, max at 3.0

        self.stars = [
            [x, y + (speed * self.speed), speed]
            for x, y, speed in self.stars
            if y + (speed * self.speed) < px.height
        ]

        # Add new stars to replace those that disappeared
        while len(self.stars) < self.stars_max:
            self.stars.append([random.randint(0, px.width), 0, random.uniform(2, 4)])

    def draw(self):
        """Draw the stars on the screen."""
        for x, y, _ in self.stars:
            px.pset(x, y, 7)  # White stars
