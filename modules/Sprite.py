# -*- coding: utf-8 -*-
# type: ignore
# modules/Sprite.py
import pgzrun
import math
import random
from pgzero.builtins import Actor   
from pygame import Rect

class SpriteManager:
    """Utility class to manage sprite operations such as generating cached
    horizontally-flipped surfaces for actors.
    """

    _flipped_cache = {}
    
    @classmethod
    def flip_image_horizontal(cls, image_name):
        """Flip an image horizontally and cache the resulting surface.

        Uses a temporary Actor to access the underlying surface. The result is
        stored in an internal cache so repeated flips are fast.
        """
        if image_name in cls._flipped_cache:
            return cls._flipped_cache[image_name]
        
        # Create a temporary Actor to access the surface
        temp_actor = Actor(image_name)
        surface = temp_actor._surf
        
        width = surface.get_width()
        height = surface.get_height()
        flipped_surface = surface.copy()
        
        # Flip horizontal pixel by pixel (safe fallback if other helpers are not
        # available in the runtime environment).
        for x in range(width):
            for y in range(height):
                mirrored_x = width - 1 - x
                color = surface.get_at((mirrored_x, y))
                flipped_surface.set_at((x, y), color)
        
        # Save in cache
        cls._flipped_cache[image_name] = flipped_surface
        return flipped_surface
    
    @classmethod
    def preload_flipped_frames(cls, frame_list):
        """Preload all horizontally flipped versions for the given frame list.

        Returns a dict mapping original frame names to their flipped surfaces.
        """
        flipped_frames = {}
        for frame in frame_list:
            flipped_frames[frame] = cls.flip_image_horizontal(frame)
        return flipped_frames

# Compatibility helper
def flip_image_horizontal(image_name):
    return SpriteManager.flip_image_horizontal(image_name)