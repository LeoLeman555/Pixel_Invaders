import json
import pyxel as px


class Menu:
    def __init__(self, main):
        """Initialize the menu."""
        self.main = main
        self.stats_frame_count = 0
        self.game_over_frame_count = 0

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
            px.text(2, 110, "PRESS 'S' TO START", 7)
            px.text(2, 120, "PRESS 'Q' TO QUIT", 7)

    def draw_game_over(self):
        """Draw the animated game over screen with statistics and restart options."""
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
            px.text(2, 110, "PRESS 'R' TO RESTART", 7)
            px.text(2, 120, "PRESS 'Q' TO QUIT", 7)
