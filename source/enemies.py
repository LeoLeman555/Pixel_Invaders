import pyxel as px


class EnemiesManager:
    """Handle the creation and movement of enemies."""

    # Constants for configuration
    ROW_SPACING = 2
    COLUMN_SPACING = 10
    INITIAL_Y = 10
    ENEMY_SPEED = 1

    def __init__(self, main):
        self.main = main

        # Load enemy sprite into image bank 1
        px.image(1).load(0, 0, "assets/images/enemy_1.png")

        # "enemy_id": [pyxel image_bank, width, height]
        self.enemy_data = [{"image_bank": 1, "width": 9, "height": 9}]

        # Active enemies list as dictionaries
        self.enemies = []
        self.speed = self.ENEMY_SPEED  # Horizontal movement speed

    def create_wave(self, enemy_id: int, num_enemies: int = 5, num_rows: int = 1) -> None:
        """Create a wave of enemies with optional rows."""
        if not (0 <= enemy_id < len(self.enemy_data)):
            print(f"Invalid enemy_id: {enemy_id}")
            return

        enemy_info = self.enemy_data[enemy_id]
        wave_width = (num_enemies - 1) * (px.width // num_enemies) + enemy_info["width"]
        start_x = (px.width - wave_width) // 2

        for row in range(num_rows):
            for i in range(num_enemies):
                x = start_x + i * (px.width // num_enemies)
                y = self.INITIAL_Y + row * (enemy_info["height"] + self.ROW_SPACING)
                self.enemies.append({
                    "x": x,
                    "y": y,
                    "image_bank": enemy_info["image_bank"],
                    "width": enemy_info["width"],
                    "height": enemy_info["height"]
                })

    def move_enemies(self):
        """Move all enemies horizontally and adjust if they reach screen edges."""
        if not self.enemies:
            return

        # Check if any enemy touches the screen edges
        edge_hit = any(
            enemy["x"] + enemy["width"] >= px.width or enemy["x"] <= 0
            for enemy in self.enemies
        )

        # Reverse direction and move enemies down if edge hit
        if edge_hit:
            self.speed = -self.speed
            for enemy in self.enemies:
                enemy["y"] += self.ROW_SPACING

        # Move enemies horizontally
        for enemy in self.enemies:
            enemy["x"] += self.speed

    def is_collision(self, enemy, laser) -> bool:
        """Check if a laser collides with an enemy."""
        return (
            enemy["x"] <= laser[0] <= enemy["x"] + enemy["width"]
            and enemy["y"] <= laser[1] <= enemy["y"] + enemy["height"]
        )

    def delete_enemy(self):
        """Remove enemies that are hit by lasers."""
        for laser in self.main.laser_manager.lasers[:]:
            for enemy in self.enemies[:]:
                if self.is_collision(enemy, laser):
                    self.enemies.remove(enemy)
                    self.main.laser_manager.lasers.remove(laser)

    def draw_enemies(self):
        """Draw all active enemies."""
        for enemy in self.enemies:
            px.blt(enemy["x"], enemy["y"], enemy["image_bank"], 0, 0, enemy["width"], enemy["height"], 0)
