import pyxel as px


class Boost:
    """Represent a boost item in the game."""

    def __init__(self, main, x, y, vx, vy, boost_type):
        self.main = main
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.vx = vx
        self.vy = vy
        self.type = boost_type
        self.active = True

    def is_collision_player(self, player):
        """Check if the boost collides with the player."""
        return (
            self.x < player.x + player.width
            and self.x + self.width > player.x
            and self.y < player.y + player.height
            and self.y + self.height > player.y
        )

    def update(self):
        """Update the position and checks for collisions."""
        self.x += self.vx
        self.y += self.vy
        if self.x <= 0 or self.x >= px.width - self.width:
            self.vx *= -1  # Reverse direction on wall collision
        if self.is_collision_player(self.main.player):
            self.active = False
            self.main.boosts_manager.activate_boost(
                self.main.boosts_manager.boosts_names[self.type]
            )
        elif self.y > px.height:
            self.active = False

    def draw(self):
        """Draw on the screen."""
        px.blt(self.x, self.y, 2, self.type * self.width, 0, self.width, self.height, 0)
