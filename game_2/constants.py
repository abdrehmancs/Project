import pygame

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

# Physics
GRAVITY = 0.8
FRICTION = 0.9
WALK_SPEED = 7
JUMP_FORCE = -20

# Combat
MAX_HEALTH = 100
ATTACK_COOLDOWN = 300 # ms
KNOCKBACK_FORCE = 15
SUPER_METER_MAX = 100
SUPER_COST_SPECIAL = 40
COMBO_WINDOW = 500 # ms
COMBO_MULTIPLIER_STEP = 0.1 # Add 10% damage per combo hit
KNOCKBACK_SUPER = 25

# Defense
BLOCK_REDUCTION = 0.3 # Damage taken while blocking
PARRY_WINDOW = 150 # ms to trigger a parry
PARRY_STUN = 60 # frames of stun for the attacker

# Menu
MENU_COLOR = (40, 40, 70)
BUTTON_COLOR = (70, 70, 110)
BUTTON_HOVER_COLOR = (100, 100, 160)
SELECT_COLOR = (60, 120, 60)

# Archetypes
ARCHETYPES = {
    "TITAN": {
        "health": 150,
        "speed": 5,
        "jump": -15,
        "damage_mod": 1.3,
        "size": (100, 200),
        "color": (100, 0, 0),
        "special_name": "EARTHQUAKE",
        "special_damage": 50,
        "special_knockback": 40
    },
    "GHOST": {
        "health": 70,
        "speed": 11,
        "jump": -22,
        "damage_mod": 0.7,
        "size": (60, 160),
        "color": (150, 150, 255),
        "special_name": "PHANTOM STRIKE",
        "special_damage": 30,
        "special_knockback": 10
    },
    "BALANCED": {
        "health": 100,
        "speed": 7,
        "jump": -20,
        "damage_mod": 1.0,
        "size": (80, 180),
        "color": (0, 100, 255),
        "special_name": "SURE-SHOT",
        "special_damage": 40,
        "special_knockback": 20
    }
}
