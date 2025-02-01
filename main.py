import pyxel as px
from source.enemies import *
from source.shooting import *


class Main:
    SCREEN_SIZE = 128
    SHIP_SIZE = (11, 16)

    def __init__(self):
        """Initialize the game and load resources."""
        px.init(self.SCREEN_SIZE, self.SCREEN_SIZE, "Pixel Invaders")

        # Load the ship image
        px.image(0).load(0, 0, "assets/images/player_ship.png")

        self.reset_game()

        self.run()

    def reset_game(self):
        """Reset game variables for a new game."""
        self.x = self.SCREEN_SIZE // 2
        self.y = self.SCREEN_SIZE // 2
        self.lives = 3
        self.score = 0
        self.game_state = "playing"  # Can be 'playing' or 'game_over'

        self.shooting_count = 0

        self.shooting_manager = ShootingManager(self)
        self.enemies_manager = EnemiesManager(self)

    def update(self):
        """Update game logic."""
        if self.game_state == "playing":
            self.update_playing()
        elif self.game_state == "game_over":
            self.update_game_over()

    def update_playing(self):
        """Update logic while the game is running."""
        if not self.enemies_manager.enemies:
            self.enemies_manager.create_wave(0, 5, 2)

        if px.btnp(px.KEY_SPACE):
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
        if px.btn(px.KEY_W) or px.btn(px.KEY_UP):
            if self.y > 0:
                self.y -= 1
        if px.btn(px.KEY_A) or px.btn(px.KEY_LEFT):
            if self.x > 0:
                self.x -= 1
        if px.btn(px.KEY_S) or px.btn(px.KEY_DOWN):
            if self.y < self.SCREEN_SIZE - self.SHIP_SIZE[1]:
                self.y += 1
        if px.btn(px.KEY_D) or px.btn(px.KEY_RIGHT):
            if self.x < self.SCREEN_SIZE - self.SHIP_SIZE[0]:
                self.x += 1

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
        self.shooting_manager.draw_lasers()
        self.shooting_manager.draw_missiles()
        self.enemies_manager.draw_enemies()

        # Management of flashing if lives are at 1
        if self.lives == 1:
            # Flashes red every 10 frames (alternating between red and invisible)
            if (px.frame_count // 10) % 2 == 0:
                px.text(2, 2, f"LIVES : {self.lives}", px.COLOR_RED)
        else:
            # Displays lives normally
            px.text(2, 2, f"LIVES : {self.lives}", 7)

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
