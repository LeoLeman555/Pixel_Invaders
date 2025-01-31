import pyxel as px
import math


class LaserManager:
    """Handle the creation and movement of lasers and missiles."""

    def __init__(self, main):
        self.main = main
        self.lasers = []
        self.missiles = []

    def create_laser(
        self,
        laser_width: int,
        laser_height: int,
        laser_color: int,
        ship_x: int,
        ship_y: int,
        ship_width: int,
    ) -> None:
        """Create a new laser at the center of the ship's position."""
        laser_x = ship_x + ship_width // 2
        laser_y = ship_y
        self.lasers.append([laser_x, laser_y, laser_width, laser_height, laser_color])

    def create_missile(self, ship_x, ship_y):
        """"Create a missile that heads for the nearest enemy."""
        if not self.main.enemies_manager.enemies:
            return 

        # Find the nearest enemy
        closest_enemy = min(
            self.main.enemies_manager.enemies,
            key=lambda enemy: math.dist((ship_x, ship_y), (enemy["x"], enemy["y"])),
        )

        missile_x = ship_x
        missile_y = ship_y

        # Direction calculation
        dx = closest_enemy["x"] - missile_x
        dy = closest_enemy["y"] - missile_y
        distance = math.sqrt(dx**2 + dy**2)

        # Normalisation to obtain a directional vector
        if distance == 0:
            return  # To avoid a division by zero if the enemy is exactly on the player
        dx /= distance
        dy /= distance

        # Add the missile with its direction
        self.missiles.append(
            {"x": missile_x, "y": missile_y, "dx": dx, "dy": dy, "speed": 5}
        )

    def move_lasers(self):
        for laser in self.lasers[:]:  # Iterate over a copy to avoid modification issues
            laser[1] -= 5  # Move the laser upward
            if laser[1] < 0:  # Remove if off-screen
                self.lasers.remove(laser)

    def move_missiles(self):
        for missile in self.missiles:
            missile["x"] += missile["dx"] * missile["speed"]
            missile["y"] += missile["dy"] * missile["speed"]

            # Delete the missile if it leaves the screen
            if (
                missile["y"] < 0
                or missile["y"] > px.height
                or missile["x"] < 0
                or missile["x"] > px.width
            ):
                self.missiles.remove(missile)

    def draw_lasers(self):
        """Drawing lasers."""
        for laser in self.lasers:
            px.rect(*laser)

    def draw_missiles(self):
        """Drawing missiles."""
        for missile in self.missiles:
            px.circ(missile["x"], missile["y"], 1, 8)  # Little circle
