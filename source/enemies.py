import pyxel as px


class EnemiesManager:
    """Handle the creation and movement of enemies."""

    # Constants for configuration
    ROW_SPACING = 2
    COLUMN_SPACING = 10
    INITIAL_Y = 10

    def __init__(self, main):
        self.main = main
        # "enemy_id": [pyxel image_bank, width, height]
        self.enemy_data = [{"image_bank": 1, "width": 9, "height": 9}]
        # Active enemies list as dictionaries
        self.enemies = []

    def create_wave(
        self, enemy_id: int, num_enemies: int = 5, num_rows: int = 1
    ) -> None:
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
                self.enemies.append(
                    {
                        "x": x,
                        "y": y,
                        "image_bank": enemy_info["image_bank"],
                        "width": enemy_info["width"],
                        "height": enemy_info["height"],
                    }
                )

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
            self.main.enemies_speed = -self.main.enemies_speed
            for enemy in self.enemies:
                enemy["y"] += self.ROW_SPACING

        # Move enemies horizontally
        for enemy in self.enemies:
            enemy["x"] += self.main.enemies_speed

            # Check if an enemy reaches the bottom of the screen
            if enemy["y"] + enemy[
                "height"
            ] >= px.height or self.is_collision_with_player(enemy):
                self.main.lose_life()
                self.enemies.remove(enemy)

    def is_collision_with_laser(self, enemy, laser) -> bool:
        """Check if a laser collides with an enemy."""
        return (
            enemy["x"] <= laser[0] <= enemy["x"] + enemy["width"]
            and enemy["y"] <= laser[1] <= enemy["y"] + enemy["height"]
        )

    def is_collision_with_missile(self, enemy, missile) -> bool:
        """Check if a missile collides with an enemy."""
        missile_radius = 1  # Missile radius

        return (
            enemy["x"] < missile["x"] + missile_radius
            and enemy["x"] + enemy["width"] > missile["x"] - missile_radius
            and enemy["y"] < missile["y"] + missile_radius
            and enemy["y"] + enemy["height"] > missile["y"] - missile_radius
        )

    def is_collision_with_player(self, enemy) -> bool:
        """Check if an enemy collides with the player."""
        player_x, player_y = self.main.x, self.main.y
        player_width, player_height = self.main.SHIP_SIZE

        return (
            enemy["x"] < player_x + player_width
            and enemy["x"] + enemy["width"] > player_x
            and enemy["y"] < player_y + player_height
            and enemy["y"] + enemy["height"] > player_y
        )

    def delete_enemy(self):
        """Remove enemies that are hit by lasers or a missile."""
        for laser in self.main.shooting_manager.lasers[:]:
            for enemy in self.enemies[:]:
                if self.is_collision_with_laser(enemy, laser):
                    self.enemies.remove(enemy)
                    self.main.shooting_manager.lasers.remove(laser)
                    self.main.score += 10

        for missile in self.main.shooting_manager.missiles[:]:
            for enemy in self.enemies[:]:
                if self.is_collision_with_missile(enemy, missile):
                    self.enemies.remove(enemy)
                    self.main.score += 10

    def draw_enemies(self):
        """Draw all active enemies."""
        for enemy in self.enemies:
            px.blt(
                enemy["x"],
                enemy["y"],
                enemy["image_bank"],
                0,
                0,
                enemy["width"],
                enemy["height"],
                0,
            )
