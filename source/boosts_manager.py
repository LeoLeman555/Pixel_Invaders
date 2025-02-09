import random
import pyxel as px
from source.boost import *


class BoostsManager:
    def __init__(self, main):
        """Initialize boost manager with boost data and references to the game."""
        self.main = main
        self.boosts_data = {
            "speed": {"time": 0, "max_time": 200, "color": 11},
            "rapid_fire": {"time": 0, "max_time": 175, "color": 9},
            "extra_life": {"time": 0, "max_time": 50, "color": 8},
            "big_shoot": {"time": 0, "max_time": 100, "color": 12},
            "enemies_slow": {"time": 0, "max_time": 150, "color": 10},
        }
        self.boosts_names = list(self.boosts_data.keys())
        self.boosts = []

    def spawn_boost(self):
        """Create a new falling boost at a random position."""
        x = random.randint(20, px.width - 20)
        vx = random.choice([-2, -1, 0, 1, 2])
        vy = random.randint(1, 2)
        boost_type = random.randint(0, len(self.boosts_names) - 1)
        self.boosts.append(Boost(self.main, x, 0, vx, vy, boost_type))

    def activate_boost(self, boost_name: str):
        """Activate a boost and reset its timer to maximum."""
        if boost_name in self.boosts_data:
            self.boosts_data[boost_name]["time"] = self.boosts_data[boost_name][
                "max_time"
            ]

    def apply_boosts(self):
        """Apply the effects of active boosts."""
        self.main.player.speed = 5 if self.boosts_data["speed"]["time"] > 0 else 2
        self.main.shooting_manager.is_big_shoot = (
            self.boosts_data["big_shoot"]["time"] > 0
        )

        if self.boosts_data["rapid_fire"]["time"] > 0:
            self.main.shooting_manager.heat = 0

        if self.boosts_data["extra_life"]["time"] > 0:
            if not self.main.extra_life_given and self.main.player.lives < 5:
                self.main.player.lives += 1
                self.main.extra_life_given = True
        else:
            self.main.extra_life_given = False

        if self.boosts_data["enemies_slow"]["time"] > 0:
            self.main.enemies_speed = 0.1 if self.main.enemies_speed > 0 else -0.1
        else:
            self.main.enemies_speed = 1 if self.main.enemies_speed > 0 else -1

    def update(self):
        """Update boosts positions and timers."""
        if len(self.boosts) <= 1 and random.random() <= 0.005:
            self.spawn_boost()

        for boost in self.boosts[:]:
            boost.update()
        self.boosts = [boost for boost in self.boosts if boost.active]

        for bar in self.boosts_data.values():
            if bar["time"] > 0:
                bar["time"] -= 1

        self.apply_boosts()

    def draw(self):
        """Draw all active boosts and their timers."""
        for boost in self.boosts:
            boost.draw()

        y_position = 12  # Start position for boost bars
        for name, bar in self.boosts_data.items():
            if bar["time"] > 0:
                bar_width = (bar["time"] / bar["max_time"]) * 124  # Scale bar width
                px.rect(2, y_position, bar_width, 1, bar["color"])  # Draw bar
                y_position += 3  # Offset for next bar
