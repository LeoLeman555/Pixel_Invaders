import pyxel as px


class Laser:
    def __init__(self, x: int, y: int, width: int, height: int, color: int, speed: int):
        """Initialize a laser with position, size, color, and speed."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.laser_speed = speed
        self.damage = 1
        self.active = True

    def update(self):
        """Move the laser up."""
        self.y -= self.laser_speed
        if self.y > px.height:
            self.active = False

    def draw(self):
        """Draw the laser."""
        px.rect(self.x, self.y, self.width, self.height, self.color)


class Missile:
    def __init__(self, x: int, y: int, dx: int, dy: int):
        """Initialize a missile with position, direction, and default properties."""
        self.x = x
        self.y = y
        self.width = 2
        self.height = 2
        self.dx = dx
        self.dy = dy
        self.speed = 7
        self.damage = 2
        self.active = True

    def update(self):
        """Move the missile with its vector and deactivate if off-screen."""
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        # Deactivate the missile if it leaves the screen
        if self.y < 0 or self.y > px.height or self.x < 0 or self.x > px.width:
            self.active = False

    def draw(self):
        """Draw the missile."""
        px.circ(self.x, self.y, 1, 8)
