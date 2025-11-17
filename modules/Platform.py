# -*- coding: utf-8 -*-
# type: ignore
import pgzrun

from modules.Enemy import Enemy
from pygame import Rect

class Platform:
    """Class that stores platform data and optionally spawns an enemy on it."""
    def __init__(self, x, y, width, height, has_enemy=False):
        self.rect = Rect(x, y, width, height)
        self.has_enemy = has_enemy
        self.enemy = None
        
        # Calculate the platform center
        self.center_x = x + width // 2
        self.center_y = y - 32
        
        # Calculate patrol bounds (leave 10px margin at edges)
        self.patrol_min = x 
        self.patrol_max = x + width - 10
        self.patrol_width = self.patrol_max - self.patrol_min
    
    def spawn_enemy(self):
        """Create an enemy at the center of this platform if configured.

        Returns the created Enemy or None if no enemy was spawned.
        """
        if self.has_enemy and self.enemy is None:
            # Cria o enemy no centro da plataforma
            enemy = Enemy(self.center_x, self.center_y, patrol_width=0)
            
            # Configura os limites de patrulha manualmente
            enemy.patrol_min_x = self.patrol_min
            enemy.patrol_max_x = self.patrol_max
            enemy.ground_y = self.center_y
            
            self.enemy = enemy
            return enemy
        else:
            return None

