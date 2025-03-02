import pyxel
import random

BOSS_HP = 100
BOSS_SPEED = 0.5
MOVE_INTERVAL = 60  # Boss changes direction every 60 frames


class Wall:
    """Manage a wall attack projectile from the boss."""

    def __init__(self, main, x: int, y: int):
        """Initialize a wall at a given position."""
        self.main = main
        self.x = x
        self.y = y
        self.active = True

    def is_collision_player(self, player):
        """Check if the wall collides with the player."""

        return (
            0 <= player.x <= self.x
            and 114 <= self.y <= 131
            or self.x + 35 <= player.x + player.width <= 145
            and 114 <= self.y <= 131
        )

    def update(self):
        """Move the wall downward and deactivate it if out of bounds."""
        self.y += 1
        if self.is_collision_player(self.main.player):
            self.main.player.lose_life()
            self.active = False
        if self.y >= 130:
            self.active = False

    def draw(self):
        """Draw the wall on the screen."""
        pyxel.rect(0, self.y, self.x, 2, 7)
        pyxel.rect(self.x + 35, self.y, 128, 2, 7)


class Boss2:
    """Manage the second boss in the game."""

    def __init__(self, main):
        """Initialize the second boss with default values."""
        self.main = main
        self.x = 39
        self.y = -50
        self.hp = 100
        self.move_steps = 0
        self.moving_direction = 0  # 0 = right, 1 = left
        self.steps = 0
        self.wall_x = 50
        self.wall_direction = 1
        self.walls = []
        self.active = False

    def move(self):
        """Handle the boss's movement pattern."""
        if self.y <= 30:
            self.y += BOSS_SPEED
            self.hp = BOSS_HP  # Reset HP once it enters
        else:
            if pyxel.frame_count % MOVE_INTERVAL == 0:
                self.move_steps = 0
                self.moving_direction = random.randint(0, 1)

            if self.move_steps < 10:
                if self.moving_direction == 0 and self.x <= 60:
                    if pyxel.frame_count % 6 == 0:
                        self.x += 1
                        self.move_steps += 1
                elif self.moving_direction == 1 and self.x >= 0:
                    if pyxel.frame_count % 6 == 0:
                        self.x -= 1
                        self.move_steps += 1

            # Ensure boss stays within boundaries
            self.x = max(0, min(self.x, 60))

    def create_wall(self):
        """Spawn walls as part of the boss's attack pattern."""
        if pyxel.frame_count % 60 == 0 and self.hp > 30 and self.y >= 20:
            spawn_x = random.randint(0, 100)
            self.walls.append(Wall(self.main, spawn_x, -2))

        if 0 < self.hp <= 30 and pyxel.frame_count % 2 == 0:
            if self.wall_direction == 0 and self.steps < 15 and self.wall_x > 3:
                self.wall_x -= 1
                self.walls.append(Wall(self.main, self.wall_x, -2))
                self.steps += 1
            elif self.wall_direction == 1 and self.steps < 15 and self.wall_x < 123:
                self.wall_x += 1
                self.walls.append(Wall(self.main, self.wall_x + 1, -2))
                self.steps += 1
            if self.wall_x >= 120:
                self.wall_direction = 0
                self.steps = 0
            elif self.wall_x <= 5:
                self.wall_direction = 1
                self.steps = 0
            elif self.steps > 14:
                self.steps = 0
                self.wall_direction = random.randint(0, 1)

    def is_collision(self) -> bool:
        """Check if the boss is hit by a laser."""
        for laser in self.main.shooting_manager.lasers:
            if (
                self.x - 3 <= laser.x <= self.x + 47
                and self.y <= laser.y <= self.y + 25
            ):
                laser.active = False
                if not self.main.shooting_manager.is_big_shoot:
                    self.main.successful_shots += 1
                self.hp -= laser.damage

    def update(self):
        """Update all boss behaviors."""
        self.move()
        self.is_collision()
        self.create_wall()

        for wall in self.walls:
            wall.update()
        self.walls = [wall for wall in self.walls if wall.active]

        if self.hp <= 0:
            self.boss_active = False
            self.__init__(self.main)

    def draw(self):
        """Draw the boss, walls, and visual effects."""
        # Draw walls
        for wall in self.walls:
            wall.draw()

        # Draw boss
        pyxel.blt(self.x, self.y, 1, 129, 0, 50, 50, 0)

        # Draw health bar
        pyxel.rect(self.x + 7, self.y - 6, 35, 4, 8)
        pyxel.rect(self.x + 7, self.y - 6, 35 * (self.hp / 100), 4, 11)

        # Display "incoming" warning
        if (pyxel.frame_count // 15) % 2 == 0 and self.y <= 20:
            pyxel.blt(28, 30, 1, 0, 16, 80, 16, 0)
