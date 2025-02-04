import pyxel as px
from source.boost import *
from source.enemies import *
from source.shooting import *


class Main:
    SCREEN_SIZE = 128
    SHIP_SIZE = (11, 16)

    def __init__(self):
        """Initialize the game and load resources."""
        px.init(self.SCREEN_SIZE, self.SCREEN_SIZE, "Pixel Invaders")

        # Load the all the images
        px.images[0].load(0, 0, "assets/images/player_ship.png")
        px.images[1].load(0, 0, "assets/images/enemy_1.png")
        px.images[2].load(0, 0, "assets/images/boost_spritesheet.png")

        self.reset_game()

        self.run()

    def reset_game(self):
        """Reset game variables for a new game."""
        self.x = self.SCREEN_SIZE // 2 - self.SHIP_SIZE[0] // 2
        self.y = self.SCREEN_SIZE - self.SHIP_SIZE[1]
        self.lives = 5
        self.score = 0
        self.game_state = "playing"  # Can be 'playing' or 'game_over'

        self.shooting_count = 0
        self.heat = 0  # Heat gauge
        self.max_heat = 10  # Overheating threshold
        self.cooldown = 0  # Waiting time in the event of overheating

        self.ship_speed = 2
        self.enemies_speed = 1
        self.extra_life_given = False
        self.is_big_shoot = False

        self.shooting_manager = ShootingManager(self)
        self.enemies_manager = EnemiesManager(self)
        self.boosts_manager = BoostsManager(self)

    def update(self):
        """Update game logic."""
        if self.game_state == "playing":
            self.update_playing()
        elif self.game_state == "game_over":
            self.update_game_over()

    def update_playing(self):
        """Update logic while the game is running."""
        if not self.enemies_manager.enemies:
            self.enemies_manager.create_wave(0, 7, 4)

        if self.is_big_shoot:
            side = px.frame_count % 6
            if side == 0:
                self.shooting_manager.create_laser(
                    1, 5, 1, self.x, self.y + self.SHIP_SIZE[0] // 2, 0
                )
            elif side == 3:
                self.shooting_manager.create_laser(
                    1,
                    5,
                    1,
                    self.x + self.SHIP_SIZE[0],
                    self.y + self.SHIP_SIZE[0] // 2,
                    0,
                )
        else:
            if (
                px.btnp(px.KEY_SPACE)
                and self.heat < self.max_heat
                and self.cooldown == 0
            ):
                if self.shooting_count % 20 == 10:
                    self.shooting_manager.create_missile(
                        self.x, self.y + self.SHIP_SIZE[0] // 2
                    )
                    self.shooting_manager.create_missile(
                        self.x + self.SHIP_SIZE[0], self.y + self.SHIP_SIZE[0] // 2
                    )
                else:
                    self.shooting_manager.create_laser(
                        1, 3, 10, self.x, self.y, self.SHIP_SIZE[0]
                    )
                self.shooting_count += 1
                self.heat += 2  # Each shot increases the heat`

        self.boosts_manager.update_boosts()
        self.boosts_manager.apply_boosts()
        self.shooting_manager.overheating()
        self.shooting_manager.move_lasers()
        self.shooting_manager.move_missiles()
        self.enemies_manager.move_enemies()
        self.enemies_manager.delete_enemy()
        self.move()

    def update_game_over(self):
        """Handle input during the game over screen."""
        if px.btnp(px.KEY_R):
            self.reset_game()
        if px.btnp(px.KEY_Q):
            px.quit()

    def move(self):
        """Handle player movement."""
        if px.btn(px.KEY_A) or px.btn(px.KEY_LEFT):
            if self.x > 0:
                self.x -= self.ship_speed
        if px.btn(px.KEY_D) or px.btn(px.KEY_RIGHT):
            if self.x < self.SCREEN_SIZE - self.SHIP_SIZE[0]:
                self.x += self.ship_speed

    def lose_life(self):
        """Reduce player lives and check for game over."""
        self.lives -= 1
        if self.lives <= 0:
            self.game_state = "game_over"

    def draw(self):
        """Render game elements on the screen."""
        px.cls(0)
        if self.game_state == "playing":
            self.draw_playing()
        elif self.game_state == "game_over":
            self.draw_game_over()

    def draw_playing(self):
        """Draw the game screen."""
        px.blt(self.x, self.y, 0, 0, 0, self.SHIP_SIZE[0], self.SHIP_SIZE[1] + 2)
        self.enemies_manager.draw_enemies()
        self.shooting_manager.draw_lasers()
        self.shooting_manager.draw_missiles()
        self.shooting_manager.draw_overheating()
        self.boosts_manager.draw_boosts()

        # Displays lives
        if self.lives > 1 or (self.lives == 1 and (px.frame_count // 10) % 2 == 0):
            for i in range(self.lives):
                px.blt(1 + i * 8, 1, 2, 80, 0, 8, 8, 0)

        # Displays the score
        px.text(75, 2, f"SCORE : {self.score}", 7)

    def draw_game_over(self):
        """Draw the game over screen."""
        if (px.frame_count // 10) % 2 == 0:
            px.text(30, 20, "--- GAME OVER ---", 7)
            px.text(30, 40, f"SCORE: {self.score}", 7)
            px.text(2, 110, "PRESS 'R' TO RESTART", 7)
            px.text(2, 120, "PRESS 'Q' TO QUIT", 7)

    def run(self):
        """Start the game loop."""
        px.run(self.update, self.draw)


if __name__ == "__main__":
    Main()
