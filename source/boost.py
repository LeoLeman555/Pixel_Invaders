import random
import pyxel as px


class BoostsManager:
    def __init__(self, main):
        """Initialize boost manager with boost data and references to the game."""
        self.main = main
        self.boosts = []
        self.boosts_data = {
            "speed": {"time": 0, "max_time": 200, "color": 11},
            "rapid_fire": {"time": 0, "max_time": 175, "color": 9},
            "extra_life": {"time": 0, "max_time": 50, "color": 8},
            "big_shoot": {"time": 0, "max_time": 100, "color": 12},
            "enemies_slow": {"time": 0, "max_time": 150, "color": 10},
        }
        self.boosts_names = list(self.boosts_data.keys())

    def spawn_boost(self):
        """Create a new falling boost at a random position."""
        x = random.randint(20, px.width - 20)
        vx = random.choice([-2, -1, 0, 1, 2])
        vy = random.randint(1, 2)
        boost_type = random.randint(0, len(self.boosts_names) - 1)
        self.boosts.append({"x": x, "y": 0, "vx": vx, "vy": vy, "type": boost_type})

    def activate_boost(self, boost_name: str):
        """Activate a boost and reset its timer to maximum."""
        if boost_name in self.boosts_data:
            self.boosts_data[boost_name]["time"] = self.boosts_data[boost_name][
                "max_time"
            ]

    def apply_boosts(self):
        """Apply the effects of active boosts."""
        self.main.ship_speed = 5 if self.boosts_data["speed"]["time"] > 0 else 2
        self.main.is_big_shoot = self.boosts_data["big_shoot"]["time"] > 0

        if self.boosts_data["rapid_fire"]["time"] > 0:
            self.main.heat = 0

        if self.boosts_data["extra_life"]["time"] > 0:
            if not self.extra_life_given and self.main.lives < 5:
                self.main.lives += 1
                self.extra_life_given = True
        else:
            self.extra_life_given = False

        if self.boosts_data["enemies_slow"]["time"] > 0:
            self.main.enemies_speed = 0.1 if self.main.enemies_speed > 0 else -0.1
        else:
            self.main.enemies_speed = 1 if self.main.enemies_speed > 0 else -1

    def is_collision_with_player(self, boost) -> bool:
        """Check if a boost collides with the player."""
        player_x, player_y = self.main.x, self.main.y
        player_width, player_height = self.main.SHIP_SIZE

        return (
            boost["x"] < player_x + player_width
            and boost["x"] + 16 > player_x
            and boost["y"] < player_y + player_height
            and boost["y"] + 16 > player_y
        )

    def delete_boost(self):
        """Remove boosts if collected by the player or if out of bounds."""
        for boost in self.boosts[:]:  # Copy list to avoid modifying during iteration
            if self.is_collision_with_player(boost):
                self.boosts.remove(boost)
                self.activate_boost(self.boosts_names[boost["type"]])
            elif boost["y"] > px.height:
                self.boosts.remove(boost)

    def update_boosts(self):
        """Update boost positions and timers."""
        if len(self.boosts) <= 1 and random.random() <= 0.005:
            self.spawn_boost()

        for boost in self.boosts[:]:
            boost["x"] += boost["vx"]
            boost["y"] += boost["vy"]

            if boost["x"] <= 0 or boost["x"] >= px.width - 16:
                boost["vx"] *= -1  # Reverse direction on wall collision

        for boost in self.boosts_data.values():
            if boost["time"] > 0:
                boost["time"] -= 1

        self.delete_boost()

    def draw_boosts(self):
        """Draw all active boosts and their timers."""
        for boost in self.boosts:
            sprite_x = boost["type"] * 16  # Offset sprite based on type
            px.blt(boost["x"], boost["y"], 2, sprite_x, 0, 16, 16, 0)

        y_position = 12  # Start position for boost bars
        for name, boost in self.boosts_data.items():
            if boost["time"] > 0:
                bar_width = (boost["time"] / boost["max_time"]) * 124  # Scale bar width
                px.rect(2, y_position, bar_width, 1, boost["color"])  # Draw bar
                y_position += 3  # Offset for next bar
