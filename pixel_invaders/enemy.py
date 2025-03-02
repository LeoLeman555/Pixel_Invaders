class Enemy:
    """Represent an enemy character in the game."""

    def __init__(self, x, y, id, enemy_type):
        self.x = x
        self.y = y
        self.id = id
        self.start_x = enemy_type["start_x"]
        self.start_y = enemy_type["start_y"]
        self.width = enemy_type["width"]
        self.height = enemy_type["height"]
        self.lives = enemy_type["lives"]
        self.score = enemy_type["score"]

    def move(self, dx, dy):
        """Move the enemy by dx, dy."""
        self.x += dx
        self.y += dy

    def is_collision(self, obj_x, obj_y, obj_width, obj_height):
        """Check if this enemy collides with another object."""
        return (
            self.x < obj_x + obj_width
            and self.x + self.width > obj_x
            and self.y < obj_y + obj_height
            and self.y + self.height > obj_y
        )
