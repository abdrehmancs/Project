import pygame
import random
from constants import *

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self._load_sounds()

    def _load_sounds(self):
        """
        Loads sound files. Since we are in a development environment,
        we'll use procedural sound generation or placeholders if files are missing.
        """
        # Define the sounds we want
        sound_files = {
            'hit_light': 'assets/sounds/hit_light.wav',
            'hit_heavy': 'assets/sounds/hit_heavy.wav',
            'jump': 'assets/sounds/jump.wav',
            'special': 'assets/sounds/special.wav'
        }

        for name, path in sound_files.items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except:
                # Create a dummy sound if the file doesn't exist to prevent crashes
                print(f"Warning: Sound file {path} not found. Using placeholder.")
                self.sounds[name] = self._create_placeholder_sound()

    def _create_placeholder_sound(self):
        """Generates a very short beep as a placeholder."""
        # Simple square wave generation
        sample_rate = 44100
        duration = 0.1
        n_samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(n_samples):
            val = 127 if (i // 10) % 2 == 0 else -127
            buf.append(val + 128)

        sound = pygame.mixer.Sound(buffer=buf)
        return sound

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()
