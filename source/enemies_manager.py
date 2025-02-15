import random
import pyxel as px
from source.enemy import *
from source.enemy_bullet import *


class EnemiesManager:
    """Handle the creation and movement of enemies."""

    ROW_SPACING = 2
    INITIAL_Y = 20

    def __init__(self, main):
        """Initialize the enemy manager."""
        self.main = main
        self.enemy_data = [
            {
                "start_x": 16,
                "start_y": 0,
                "width": 9,
                "height": 9,
                "lives": 1,
                "score": 10,
            },
            {
                "start_x": 48,
                "start_y": 0,
                "width": 10,
                "height": 10,
                "lives": 2,
                "score": 30,
            },
        ]
        self.enemies = []
        self.enemy_lasers = []

    def create_wave(self, num_enemies: int = 1, num_rows: int = 1, enemies_id: int = 0):
        """Create a wave of enemies."""
        enemy_info = self.enemy_data[enemies_id]
        wave_width = (num_enemies - 1) * (px.width // num_enemies) + enemy_info["width"]
        start_x = (px.width - wave_width) // 2
        for row in range(num_rows):
            for i in range(num_enemies):
                x = start_x + i * (px.width // num_enemies)
                y = self.INITIAL_Y + row * (enemy_info["height"] + self.ROW_SPACING)
                self.enemies.append(Enemy(x, y, enemies_id, enemy_info))

    def move_enemies(self):
        """Move all enemies and check collisions."""
        # Check if an enemy touches the edge
        edge_hit = any(
            enemy.x + enemy.width >= px.width or enemy.x <= 0 for enemy in self.enemies
        )

        if edge_hit:
            self.main.enemies_speed = -self.main.enemies_speed
            for enemy in self.enemies:
                enemy.move(0, self.ROW_SPACING)

        for enemy in self.enemies[:]:  # Copy the list to avoid looping deletions
            enemy.move(self.main.enemies_speed, 0)
            if enemy.y + enemy.height >= px.height or self.check_collision(
                enemy, self.main.player
            ):
                self.main.player.lose_life()
                self.enemies.remove(enemy)

    def enemy_shoot(self):
        """Make a random enemy fire a laser."""
        enemy = random.choice(self.enemies)
        self.enemy_lasers.append(
            EnemyLaser(self.main, enemy.x + enemy.width // 2, enemy.y + enemy.height)
        )

    def check_collision(self, enemy, obj):
        """Check if an enemy collides with an object."""
        return enemy.is_collision(obj.x, obj.y, obj.width, obj.height)

    def delete_enemy(self):
        """Remove enemies that are hit by lasers or missiles."""
        for laser in self.main.shooting_manager.lasers[:]:
            for enemy in self.enemies[:]:
                if self.check_collision(enemy, laser):
                    enemy.lives -= laser.damage
                    laser.active = False
                    if not self.main.shooting_manager.is_big_shoot:
                        self.main.successful_shots += 1
                    if enemy.lives <= 0:
                        self.enemies.remove(enemy)
                        self.main.enemies_killed += 1
                        self.main.score += enemy.score

        for missile in self.main.shooting_manager.missiles[:]:
            for enemy in self.enemies[:]:
                if self.check_collision(enemy, missile):
                    enemy.lives -= missile.damage
                    self.main.successful_shots += 1
                    if enemy.lives <= 0:
                        self.enemies.remove(enemy)
                        self.main.enemies_killed += 1
                        self.main.score += enemy.score

    def update(self):
        """Update all active enemies and enemy lasers."""
        if self.enemies:
            if random.random() < 0.02:
                self.enemy_shoot()
            self.move_enemies()
            self.delete_enemy()
        else:
            if self.main.wave == self.main.max_wave:
                self.main.wave = 0
                self.main.score += 1000
            wave_data = self.main.waves_data[self.main.wave]
            if wave_data["enemy_id"] == 2:
                self.main.boss.active = True
                self.main.score += 100 * self.main.wave
                self.main.wave += 1
            else:
                if not self.main.boss.active:
                    self.create_wave(
                        wave_data["enemies_per_row"],
                        wave_data["rows"],
                        wave_data["enemy_id"],
                    )
                    self.main.score += 10 * self.main.wave
                    self.main.wave += 1
        for enemy_laser in self.enemy_lasers:
            enemy_laser.update()
        self.enemy_lasers = [laser for laser in self.enemy_lasers if laser.active]

    def draw(self):
        """Draw all active enemies and enemy lasers."""
        for enemy in self.enemies:
            px.blt(
                enemy.x,
                enemy.y,
                1,
                enemy.start_x
                + ((16 * ((px.frame_count // 10) % 2)) if enemy.id < 2 else 0),
                enemy.start_y,
                enemy.width,
                enemy.height,
                0,
            )

        for enemy_laser in self.enemy_lasers:
            enemy_laser.draw()
