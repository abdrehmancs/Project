import pygame
import sys

from settings import settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    
    def __init__(self):
        """Initialize the game and create game resources."""
        pygame.init()        
        self.clock = pygame.time.Clock()
        self.settings = settings()
        
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        
        pygame.display.set_caption("Alien Invasion")
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()


        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self.aliens.update()
            
            #Get rid of bullets that have disappeared.
            self._update_bullets()
            print(len(self.bullets))  # Print the number of bullets currently on the screen
            
            
            self._update_screen()
            self.clock.tick(60)  # Limit the frame rate to 60 FPS
            
     #function to check for events like keypresses and mouse events.       
    def _check_events(self):
        """Respond to the keypresses and mouse events."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                        
    #separate function for keydown events to keep the code organized and readable.               
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
            
    #separate function for keyup events to keep the code organized and readable.
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                
                
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    #function to update the screen during each pass through the loop. It fills the screen with the background color, draws the ship, 
    # and then flips to the new screen.
    def _update_screen(self):
        """Update the images on screen and flip to the new screen"""   
    #Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
                
        #make the most recently drawn screen visible.
        pygame.display.flip()
        
        
        
    def _create_fleet(self):
        """create the fleet of aliens."""
        #create an alien and keep adding untill there is no room left
        #spacing between the alien is one width length and one alien height
        #make an alien.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.width, alien.rect.height
        
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
                
            # Finished a row; reset x value, and increment y value
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien.x = x_position
        alien.rect.x = x_position
        alien.rect.y = y_position
        self.aliens.add(alien)
        
        
    def _update_aliens(self):
        """Update the positions of all aliens in the fleet."""
        self.aliens.update()


        
        
if __name__ == '__main__':
    #make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()