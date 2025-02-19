import math
import pyxel as px
from source.player_bullet import *


class ShootingManager:
    """Handle the creation and movements of lasers and missiles."""

    def __init__(self, main):
        self.main = main
        self.player = self.main.player
        self.heat = 0  # Heat gauge
        self.max_heat = 10  # Overheating threshold
        self.cooldown = 0  # Waiting time in the event of overheating
        self.is_big_shoot = False
        self.lasers = []
        self.missiles = []

    def create_laser(self, width: int, height: int, color, speed, var_x, var_y):
        """Create a laser at the center of the ship's position."""
        x = self.player.x + var_x
        y = self.player.y + var_y
        self.lasers.append(Laser(x, y, width, height, color, speed))

    def create_missile(self, var_x: int, var_y: int):
        """Create a missile that heads for the nearest enemy."""
        if not self.main.enemies_manager.enemies:
            return

        x = self.player.x + var_x
        y = self.player.y + var_y

        # Find the nearest enemy
        closest_enemy = min(
            self.main.enemies_manager.enemies,
            key=lambda enemy: math.dist((x, y), (enemy.x, enemy.y)),
        )

        # Direction calculation
        dx = closest_enemy.x - x
        dy = closest_enemy.y - y

        # Normalization to obtain a directional vector
        distance = math.sqrt(dx**2 + dy**2)
        dx /= distance
        dy /= distance

        # Add the missile with its direction
        self.missiles.append(Missile(x, y, dx, dy))

    def overheating(self):
        """Manage the weapon overheating system."""
        if self.heat > 0:
            self.heat -= 0.1  # Heat is slowly reduced

        if self.heat >= self.max_heat:
            self.cooldown = 100  # Waiting time before firing again (60 frames)
            self.heat = self.max_heat

        if self.cooldown > 0:
            self.cooldown -= 1
            if self.cooldown == 0:
                self.heat = 0  # Resets the heat after overheating

    def update(self):
        """Update shooting mechanics, handle firing, movement, and overheating."""
        if self.is_big_shoot:
            side = px.frame_count % 6
            if side == 0:
                self.create_laser(1, 5, 5, 10, 0, self.player.height // 2)
            elif side == 3:
                self.create_laser(
                    1, 5, 5, 10, self.player.width, self.player.height // 2
                )

        if px.btnp(px.KEY_SPACE) and self.heat < self.max_heat and self.cooldown == 0:
            if self.main.shots_fired % 20 == 10:
                self.create_missile(0, self.player.height // 2)
                self.create_missile(self.player.width, self.player.height // 2)
            else:
                self.create_laser(1, 3, 10, 5, self.player.width // 2, 0)
            self.main.shots_fired += 1
            self.heat += 2  # Each shot increases the heat

        for laser in self.lasers[:]:  # Iterate over a copy to avoid modification issues
            laser.update()
        self.lasers = [laser for laser in self.lasers if laser.active]

        for missile in self.missiles[:]:
            missile.update()
        self.missiles = [missile for missile in self.missiles if missile.active]

        self.overheating()

    def draw(self):
        """Render all lasers, missiles, and overheating status."""
        for laser in self.lasers:
            laser.draw()
        for missile in self.missiles:
            missile.draw()

        px.rect(42, 3, self.heat * 3, 3, 8)
        px.rectb(42, 3, self.max_heat * 3, 3, 7)

        if self.cooldown > 0:
            if (px.frame_count // 10) % 2 == 0:
                px.text(40, 10, "OVERHEAT", 8)
