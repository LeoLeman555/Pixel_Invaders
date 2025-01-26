import pyxel as px

class LaserManager:
    """Handle the creation and movement of lasers."""
    def __init__(self):
        # List of active lasers: [x, y, width, height, color]
        self.lasers = []
    
    def create_laser(self, laser_width: int, laser_height: int, laser_color: int, ship_x: int, ship_y: int, ship_width: int) -> None:
        """Create a new laser at the center of the ship's position."""
        laser_x = ship_x + ship_width // 2
        laser_y = ship_y
        self.lasers.append([laser_x, laser_y, laser_width, laser_height, laser_color])
    
    def move_lasers(self):
        for laser in self.lasers[:]:  # Iterate over a copy to avoid modification issues
            laser[1] -= 5  # Move the laser upward
            if laser[1] < 0:  # Remove if off-screen
                self.lasers.remove(laser)
    
    def draw_lasers(self):
        """Draws all active lasers."""
        for laser in self.lasers:
            px.rect(*laser)  # Draw the laser
