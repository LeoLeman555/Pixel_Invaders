import pyxel
import random

BOSS_HP = 50
BOSS_SPEED = 0.5
MOVE_INTERVAL = 60  # Boss changes direction every 60 frames
BOMB_DROP_INTERVAL = 30  # Bombs drop every 30 frames
BOMB_SPEED = 1
EXPLOSION_LIFETIME = 9


class Bomb:
    """Represent a bomb dropped by the boss."""

    def __init__(self, main, x: int, y: int):
        self.main = main
        self.x = x
        self.y = y
        self.active = True

    def update(self):
        """Move the bomb downwards."""
        self.y += BOMB_SPEED
        if self.y >= 115:
            self.active = False
            self.main.boss.explosions.append(Explosion(self.main, self.x))

    def draw(self):
        """Draw the bomb."""
        pyxel.circ(self.x, self.y, 5, 8)
        pyxel.circ(self.x, self.y, 4, 2)


class Explosion:
    """Represent an explosion caused by a bomb hitting the ground."""

    def __init__(self, main, x: int):
        self.main = main
        self.x = x
        self.radius = EXPLOSION_LIFETIME
        self.active = True
        self.hit_player = False

    def is_collision_player(self, player):
        """Check if the boost collides with the player."""
        return (
            self.x < player.x + player.width
            and self.x + self.radius * 2 > player.x
            and 115 < player.y + player.height
            and 115 + self.radius * 2 > player.y
        )

    def update(self) -> bool:
        """Reduce the explosion size over time."""
        self.radius -= 1
        if self.is_collision_player(self.main.player) and not self.hit_player:
            self.main.player.lose_life()
            self.hit_player = True
        if self.radius <= 0:
            self.active = False

    def draw(self):
        """Draw the explosion."""
        pyxel.circ(self.x, 115, self.radius, 9)
        pyxel.circ(self.x, 115, self.radius - 1, 10)
        pyxel.circ(self.x, 115, self.radius - 3, 7)


class Boss:
    """Manage the boss enemy in the game."""

    def __init__(self, main):
        self.main = main
        self.x = 39
        self.y = -50
        self.hp = BOSS_HP
        self.moving_direction = 0  # 0 = right, 1 = left
        self.steps = 0
        self.bombs = []
        self.explosions = []
        self.active = False

    def move(self):
        """Handle the boss's movement pattern."""
        if self.y <= 30:
            self.y += BOSS_SPEED
            self.hp = BOSS_HP  # Reset HP once it enters
        else:
            if pyxel.frame_count % MOVE_INTERVAL == 0:
                self.steps = 0
                self.moving_direction = random.randint(0, 1)

            if self.steps < 10:
                if self.moving_direction == 0 and self.x <= 60:
                    if pyxel.frame_count % 6 == 0:
                        self.x += 1
                        self.steps += 1
                elif self.moving_direction == 1 and self.x >= 0:
                    if pyxel.frame_count % 6 == 0:
                        self.x -= 1
                        self.steps += 1

            # Ensure boss stays within boundaries
            self.x = max(0, min(self.x, 60))

    def create_bomb(self):
        """Drop a bomb at a random position under the boss."""
        self.bombs.append(Bomb(self.main, self.x + random.randint(0, 40), 40))

    def is_collision(self) -> bool:
        """Check if the boss is hit by a laser."""
        for laser in self.main.shooting_manager.lasers:
            if (
                self.x + 14 <= laser.x <= self.x + 33
                and self.y <= laser.y <= self.y + 13
            ):
                laser.active = False
                if not self.main.shooting_manager.is_big_shoot:
                    self.main.successful_shots += 1
                self.hp -= laser.damage

    def update(self):
        """Update all boss behaviors."""
        self.move()
        self.is_collision()

        if pyxel.frame_count % BOMB_DROP_INTERVAL == 0 and self.y >= 30 and self.hp > 0:
            self.create_bomb()

        for bomb in self.bombs:
            bomb.update()
        self.bombs = [bomb for bomb in self.bombs if bomb.active]

        for explosion in self.explosions:
            explosion.update()
        self.explosions = [
            explosion for explosion in self.explosions if explosion.active
        ]

        if self.hp <= 0:
            self.boss_active = False
            self.__init__(self.main)

    def draw(self):
        """Draw the boss, bombs, and explosions."""
        for bomb in self.bombs:
            bomb.draw()
        for explosion in self.explosions:
            explosion.draw()

        pyxel.blt(self.x, self.y, 1, 80, 0, 49, 50, 0)
        pyxel.rect(self.x + 11, self.y - 6, 27, 4, 8)  # Health bar background
        pyxel.rect(
            self.x + 11, self.y - 6, 27 * (self.hp / BOSS_HP), 4, 11
        )  # Health bar fill

        # "Incoming" warning when entering
        if (pyxel.frame_count // 15) % 2 == 0 and self.y <= 30:
            pyxel.blt(28, 30, 1, 0, 16, 80, 16, 0)
