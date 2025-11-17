# modules/Projectile.py
# -*- coding: utf-8 -*-
# type: ignore
from pygame import Rect

class Projectile:
    """Simple projectile class used by the player when attacking.

    Attributes:
        rect (pygame.Rect): rectangle representing position and size.
        direction (int): 1 for right, -1 for left.
        speed (int): horizontal speed in pixels per frame.
        color (tuple): RGB color used to draw the projectile.
        alive (bool): whether the projectile is active.
    """

    def __init__(self, x, y, direction, speed=10, width=10, height=4, color=(255, 255, 0)):
        # position and direction
        self.rect = Rect(x, y, width, height)
        self.direction = direction  # 1 = right, -1 = left
        self.speed = speed
        self.color = color
        self.alive = True

    def update(self, screen_width):
        """Move the projectile and deactivate it if it leaves the screen."""
        self.rect.x += self.speed * self.direction

        # deactivate when leaving screen bounds
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.alive = False

    def draw(self, screen):
        """Draw the projectile to the given screen object."""
        screen.draw.filled_rect(self.rect, self.color)
