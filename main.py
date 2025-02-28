import json
import pyxel as px
from source.boosts_manager import *
from source.boss import *
from source.boss_2 import *
from source.enemies_manager import *
from source.menu import *
from source.player import *
from source.shooting_manager import *
from source.starfield import *


class Main:
    def __init__(self):
        """Initialize and start the game: Pixel Invaders."""
        px.init(128, 128, "Pixel Invaders")

        with open("data/waves.json", "r") as file:
            self.waves_data = json.load(file)["waves"]

        with open("data/stats.json", "r") as file:
            self.stats = json.load(file)

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
        self.time = 0
        self.enemies_killed = 0
        self.shots_fired = 0
        self.successful_shots = 0
        self.accuracy = 0

        self.max_wave = len(self.waves_data)
        self.game_state = "menu"  # Can be 'menu' or 'playing' or 'game_over' or 'show_stats' or 'rules'

        self.enemies_speed = 1
        self.extra_life_given = False

        self.player = Player(self, px.width // 2, px.height)
        self.shooting_manager = ShootingManager(self)
        self.enemies_manager = EnemiesManager(self)
        self.boosts_manager = BoostsManager(self)
        self.boss = Boss(self)
        self.boss_2 = Boss2(self)
        self.menu = Menu(self)
        self.starfield = StarField()

    def update(self):
        """Update game logic."""
        if self.game_state == "show_stats":
            if px.btnp(px.KEY_M):
                self.game_state = "menu"
            if px.btnp(px.KEY_Q):
                px.quit()
        elif self.game_state == "rules":
            if px.btnp(px.KEY_M):
                self.game_state = "menu"
            if px.btnp(px.KEY_S):
                self.game_state = "playing"
        elif self.game_state == "playing":
            self.update_playing()
        elif self.game_state == "game_over":
            self.update_game_over()
        elif self.game_state == "menu":
            self.menu.update()

    def update_playing(self):
        """Update logic while the game is running."""
        self.starfield.update()
        if self.boss.active:
            self.boss.update()
        if self.boss_2.active:
            self.boss_2.update()
        self.player.update()
        self.boosts_manager.update()
        self.enemies_manager.update()
        self.shooting_manager.update()

        if px.frame_count % 30 == 0:
            self.time += 1

    def update_game_over(self):
        """Handle input during the game over screen."""
        if px.btnp(px.KEY_M):
            self.menu.save_stats()
            self.game_state = "menu"
        if px.btnp(px.KEY_Q):
            self.menu.save_stats()
            px.quit()

    def draw(self):
        """Render game elements on the screen."""
        px.cls(0)
        if self.game_state == "show_stats":
            self.menu.draw_stats()
        elif self.game_state == "rules":
            self.menu.draw_rules()
        elif self.game_state == "playing":
            self.draw_playing()
        elif self.game_state == "game_over":
            self.menu.draw_game_over()
        elif self.game_state == "menu":
            self.menu.draw()

    def draw_playing(self):
        """Draw the game screen."""
        self.starfield.draw()
        if self.boss.active:
            self.boss.draw()
        if self.boss_2.active:
            self.boss_2.draw()
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

    def run(self):
        """Start the game loop."""
        px.run(self.update, self.draw)


if __name__ == "__main__":
    Main()
