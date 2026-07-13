class settings:
    """A class to store all settings for the Alien Invasion"""
    
    def __init__(self):
        """Initialize the game's settings."""
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (230,230,230)
        
        
        #ship settings
        self.ship_speed = 1.5