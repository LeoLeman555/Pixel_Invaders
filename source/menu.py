import json
import pyxel as px


class Menu:
    """Represents the different menu of the game"""

    def __init__(self, main):
        self.main = main
        self.options = ["START", "RULES", "STATISTICS", "QUIT"]  # Menu options
        self.selected = 0  # Index of the currently selected option
        self.rules_frame_count = 0
        self.stats_frame_count = 0
        self.menu_frame_count = 0
        self.game_over_frame_count = 0

        self.text_offset_x = 0  # Used for small text animation
        self.text_direction = 1  # Direction of the text movement

    def update(self):
        """Handle user input and update the menu's animations."""
        # Move selection down
        if px.btnp(px.KEY_DOWN) or px.btnp(px.KEY_S):
            self.selected = (self.selected + 1) % len(self.options)

        # Move selection up
        if px.btnp(px.KEY_UP) or px.btnp(px.KEY_W) or px.btnp(px.KEY_Z):
            self.selected = (self.selected - 1) % len(self.options)

        # Handle selection confirmation
        if px.btnp(px.KEY_SPACE):
            if self.selected == 0:  # Start game
                self.main.reset_game()
                self.main.game_state = "playing"
            elif self.selected == 1:
                self.main.game_state = "rules"
            elif self.selected == 2:  # Show statistics
                self.main.game_state = "show_stats"
            elif self.selected == 3:  # Quit game
                px.quit()

        # Animate the text movement every 5 frames
        if self.menu_frame_count % 5 == 0:
            self.text_offset_x += self.text_direction

            # Reverse direction when reaching boundaries
            if self.text_offset_x > 5 or self.text_offset_x < 0:
                self.text_direction *= -1

    def draw(self):
        """Render the menu on the screen with animated elements."""
        self.menu_frame_count += 1  # Increment frame count for animations

        # Animate title appearing from top
        title_y = min(15, -10 + self.menu_frame_count)
        px.text(20, title_y, "--- PIXEL INVADERS ---", 7)

        # Create a wave-like animation effect
        wave_offset = (self.menu_frame_count // 5) % 10
        animated_menu = [("START", 40), ("RULES", 55), ("STATISTICS", 70), ("QUIT", 85)]

        # Display menu options with animation and color change
        for i, (text, y) in enumerate(animated_menu):
            x_pos = max(
                45, 100 - (self.menu_frame_count - i * 20) * 5
            )  # Smooth movement
            color = (
                10 + wave_offset // 2 if i == self.selected else 7
            )  # Highlight selected option
            px.text(x_pos, y, text, color)

        # Display instructions with small horizontal movement effect
        px.text(10 + self.text_offset_x, 110, "USE ARROW KEYS TO NAVIGATE", 7)
        px.text(10 + self.text_offset_x, 120, "PRESS 'SPACE' TO CONFIRM", 7)

    def save_stats(self):
        """Update and save the player's game statistics to a JSON file."""
        if self.main.score > self.main.stats["records"]["highscore"]:
            self.main.stats["records"]["highscore"] = self.main.score
        if self.main.wave > self.main.stats["records"]["highest_wave_reached"]:
            self.main.stats["records"]["highest_wave_reached"] = self.main.wave

        self.main.stats["global_stats"]["total_games_played"] += 1
        self.main.stats["global_stats"]["total_score"] += self.main.score
        self.main.stats["global_stats"]["average_score"] = (
            self.main.stats["global_stats"]["total_score"]
            // self.main.stats["global_stats"]["total_games_played"]
        )
        self.main.stats["global_stats"]["total_time_played"] += self.main.time
        self.main.stats["global_stats"][
            "total_enemies_killed"
        ] += self.main.enemies_killed
        self.main.stats["global_stats"]["total_waves_completed"] += self.main.wave
        self.main.stats["global_stats"][
            "total_successful_shots"
        ] += self.main.successful_shots
        self.main.stats["global_stats"]["total_shots_fired"] += self.main.shots_fired
        self.main.stats["global_stats"]["average_accuracy"] = round(
            (
                self.main.stats["global_stats"]["total_successful_shots"]
                / self.main.stats["global_stats"]["total_shots_fired"]
            )
            * 100,
            2,
        )

        with open("data/stats.json", "w") as file:
            json.dump(self.main.stats, file, indent=4)

    def draw_stats(self):
        """Display animated game statistics on the screen."""
        self.stats_frame_count += 1
        title_y = min(5, -10 + (self.stats_frame_count // 2))
        px.text(30, title_y, "--- GAME STATS ---", 7)

        wave_offset = (self.stats_frame_count // 5) % 10
        animated_stats = [
            (f"HIGHSCORE: {self.main.stats['records']['highscore']} PTS", 20),
            (f"HIGHEST WAVE: {self.main.stats['records']['highest_wave_reached']}", 30),
            (
                f"AVERAGE SCORE: {self.main.stats['global_stats']['average_score']} PTS",
                50,
            ),
            (
                f"AVERAGE ACCURACY: {self.main.stats['global_stats']['average_accuracy']} %",
                60,
            ),
            (
                f"ENEMIES KILLED: {self.main.stats['global_stats']['total_enemies_killed']}",
                80,
            ),
            (
                f"TIME PLAYED: {self.main.stats['global_stats']['total_time_played'] // 60} MIN",
                90,
            ),
        ]

        for i, (text, y) in enumerate(animated_stats):
            x_pos = max(10, 100 - (self.stats_frame_count - i * 20) * 5)
            px.text(x_pos, y, text, 7 if i % 2 == 0 else 10 + wave_offset // 2)

        if (self.stats_frame_count // 10) % 2 == 0:
            px.text(2, 110, "PRESS 'M' FOR MENU", 7)
            px.text(2, 120, "PRESS 'Q' TO QUIT", 7)

    def draw_game_over(self):
        """Draw the animated game over screen with statistics and menu options."""
        self.game_over_frame_count += 1
        title_y = min(5, -10 + (self.game_over_frame_count // 2))
        px.text(30, title_y, "--- GAME OVER ---", 7)

        wave_offset = (self.game_over_frame_count // 5) % 10
        animated_stats = [
            (f"SCORE: {self.main.score} PTS", 20),
            (f"HIGHSCORE: {self.main.stats['records']['highscore']} PTS", 30),
            (f"WAVE: {self.main.wave}", 50),
            (f"HIGHEST WAVE: {self.main.stats['records']['highest_wave_reached']}", 60),
            (
                f"ACCURACY: {round((self.main.successful_shots/self.main.shots_fired)* 100, 2)} %",
                80,
            ),
            (
                f"AVERAGE ACCURACY: {self.main.stats['global_stats']['average_accuracy']} %",
                90,
            ),
        ]

        for i, (text, y) in enumerate(animated_stats):
            x_pos = max(10, 100 - (self.game_over_frame_count - i * 20) * 5)
            px.text(x_pos, y, text, 7 if i % 2 == 0 else 10 + wave_offset // 2)

        if (self.game_over_frame_count // 10) % 2 == 0:
            px.text(2, 110, "PRESS 'M' FOR MENU", 7)
            px.text(2, 120, "PRESS 'Q' TO QUIT", 7)

    def draw_rules(self):
        """Draw the rules."""
        self.rules_frame_count += 1
        title_y = min(5, -10 + (self.rules_frame_count // 2))
        px.text(30, title_y, "--- GAME RULES ---", 7)

        wave_offset = (self.rules_frame_count // 5) % 10
        animated_text = [
            ("1. Pilot your ship with arrows", 20),
            ("2. Shoot with space bar", 30),
            ("3. Defeat enemy and boss waves", 40),
            ("4. Don't shoot too fast, or...", 50),
            ("5. Power-ups can be very useful", 60),
            ("Only one mission :", 80),
            ("- Survive as long as possible -", 90),
        ]

        for i, (text, y) in enumerate(animated_text):
            x_pos = max(3, 100 - (self.rules_frame_count - i * 40) * 5)
            px.text(x_pos, y, text, 10 + wave_offset // 2 if i > 4 else 7)

        if (self.rules_frame_count // 10) % 2 == 0:
            px.text(2, 110, "PRESS 'S' TO START", 7)
            px.text(2, 120, "PRESS 'M' TO MENU", 7)
