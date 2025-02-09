import pyxel as px
from source.boosts_manager import *
from source.enemies_manager import *
from source.player import *
from source.shooting_manager import *


class Main:
    def __init__(self):
        """Initialize and start the game: Pixel Invaders."""
        px.init(128, 128, "Pixel Invaders")

        self.waves_data = [
            [1, 1, 0],
            [2, 1, 1],
            [3, 1, 0],
            [4, 1, 0],
            [5, 1, 1],
            [6, 1, 0],
            [3, 2, 1],
            [7, 1, 0],
            [8, 1, 1],
            [4, 2, 0],
            [9, 1, 1],
            [5, 2, 0],
            [10, 1, 0],
            [6, 2, 1],
            [3, 3, 0],
            [7, 2, 0],
            [4, 3, 1],
            [8, 2, 0],
            [5, 3, 1],
            [9, 2, 0],
            [6, 3, 0],
            [10, 2, 1],
            [7, 3, 0],
            [8, 3, 1],
            [6, 4, 0],
            [9, 3, 0],
            [6, 4, 1],
            [10, 3, 0],
            [7, 4, 0],
            [8, 4, 0],
            [9, 4, 1],
            [10, 4, 0],
            [7, 5, 0],
            [8, 5, 1],
            [9, 5, 0],
            [10, 5, 1],
        ]

        # Load the all the images
        px.images[0].load(0, 0, "assets/images/player_spritesheet.png")
        px.images[1].load(0, 0, "assets/images/enemies_spritesheet.png")
        px.images[2].load(0, 0, "assets/images/boosts_spritesheet.png")

        self.reset_game()

        self.run()

    def reset_game(self):
        """Reset game variables for a new game."""
        self.score = 0
        self.wave = 0
        self.max_wave = len(self.waves_data)
        self.game_state = "playing"  # Can be 'playing' or 'game_over'

        self.enemies_speed = 1
        self.extra_life_given = False

        self.player = Player(self, px.width // 2, px.height)
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
        self.player.update()
        self.boosts_manager.update()
        self.enemies_manager.update()
        self.shooting_manager.update()

    def update_game_over(self):
        """Handle input during the game over screen."""
        if px.btnp(px.KEY_R):
            self.reset_game()
        if px.btnp(px.KEY_Q):
            px.quit()

    def draw(self):
        """Render game elements on the screen."""
        px.cls(0)
        if self.game_state == "playing":
            self.draw_playing()
        elif self.game_state == "game_over":
            self.draw_game_over()

    def draw_playing(self):
        """Draw the game screen."""
        self.shooting_manager.draw()
        self.enemies_manager.draw()
        self.boosts_manager.draw()
        self.player.draw()

        # Displays lives
        if self.player.lives > 1 or (
            self.player.lives == 1 and (px.frame_count // 10) % 2 == 0
        ):
            for i in range(self.player.lives):
                px.blt(1 + i * 8, 1, 2, 80, 0, 8, 8, 0)

        # Displays the score
        px.text(75, 2, f"SCORE : {self.score}", 7)
        px.text(75, 10, f"WAVE : {self.wave}", 7)

    def draw_game_over(self):
        """Draw the game over screen."""
        if (px.frame_count // 10) % 2 == 0:
            px.text(2, 110, "PRESS 'R' TO RESTART", 7)
            px.text(2, 120, "PRESS 'Q' TO QUIT", 7)
        px.text(30, 20, "--- GAME OVER ---", 7)
        px.text(30, 40, f"SCORE: {self.score}", 7)
        px.text(30, 50, f"WAVE : {self.wave}", 7)

    def run(self):
        """Start the game loop."""
        px.run(self.update, self.draw)


if __name__ == "__main__":
    Main()
