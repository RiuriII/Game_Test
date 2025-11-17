# -*- coding: utf-8 -*-
# type: ignore
import random
from pgzero.builtins import Actor
from pygame import Rect
from modules.Sprite import SpriteManager

class Enemy:
    def __init__(self, x, y, patrol_width=200):
        self.actor = Actor("enemy_idle1", (x, y))
        self.start_x = x
        self.ground_y = y

    # physics
        self.vel_y = 0
        self.gravity = 0.8
        self.on_ground = True

    # patrol
        half = patrol_width // 2
        self.patrol_min_x = x - half
        self.patrol_max_x = x + half
        self.speed = 2 + random.random() * 1.5
        self.direction = random.choice([-1, 1])

    # combat
        self.health = 50
        self.is_dead = False
        self.attack_damage = 10
        self.detection_radius = 10
        self.attack_range = 10
        self.attack_cooldown = 1.5
        self._time_since_last_attack = 0.0

    # animations
        self.idle_frames = ["enemy_idle1", "enemy_idle2", "enemy_idle3", "enemy_idle4"]
        self.run_frames = [
            "enemy_run1",
            "enemy_run2",
            "enemy_run3",
            "enemy_run4",
            "enemy_run5",
        ]
        self.death_frames = [
            "enemy_dead1",
            "enemy_dead2",
            "enemy_dead3",
            "enemy_dead4",
            "enemy_dead5",
            "enemy_dead6",
        ]
        self.attack_frames = [
            "enemy_attack1",
            "enemy_attack2",
            "enemy_attack3",
            "enemy_attack4",
            "enemy_attack5",
            "enemy_attack6",
        ]

        self.frame_index = 0
        self.frame_delay = 0.16
        self._anim_timer = 0.0

        # state
        self.state = "patrol"

        # Preload all flipped versions of frames into caches
        self.flipped_idle_frames = SpriteManager.preload_flipped_frames(self.idle_frames)
        self.flipped_run_frames = SpriteManager.preload_flipped_frames(self.run_frames)
        self.flipped_death_frames = SpriteManager.preload_flipped_frames(self.death_frames)
        self.flipped_attack_frames = SpriteManager.preload_flipped_frames(self.attack_frames)

        # Set initial image based on direction/state
        self._apply_directioned_image()

        # attack control
        self.is_attacking = False
        self._attack_timer = 0.0
        self.has_damaged = False  # Tracks if this attack already damaged the hero

    def update(self, dt, hero):
        if self.is_dead:
            self._update_death(dt)
            return

    # timers
        self._time_since_last_attack += dt

    # simple gravity
        self.vel_y += self.gravity
        self.actor.y += self.vel_y
        if self.actor.y >= self.ground_y:
            self.actor.y = self.ground_y
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

    # behavior
        dist_to_hero = abs(self.actor.x - hero.actor.x)
        dist_y = abs(self.actor.y - hero.actor.y)
        same_height = dist_y <= 20

        if self.is_attacking:
            # during attack, only run animation
            self._animate_attack(dt, hero)
            return

        if dist_to_hero <= self.attack_range and same_height and not hero.is_dead:
            self.state = "attack"
            self._attack(hero, dt)
        elif dist_to_hero <= self.detection_radius and same_height and not hero.is_dead:
            self.state = "chase"
            self._chase(hero, dt)
            self._animate_run(dt)
        else:
            self.state = "patrol"
            self._patrol(dt)
            self._animate_idle(dt)

    def draw(self):
        self.actor.draw()

    # -------------------------------
    # COMPORTAMENTOS
    # -------------------------------
    def _patrol(self, dt):
        self.actor.x += self.direction * self.speed
        if self.actor.x < self.patrol_min_x:
            self.actor.x = self.patrol_min_x
            self.direction = 1
        elif self.actor.x > self.patrol_max_x:
            self.actor.x = self.patrol_max_x
            self.direction = -1

    def _chase(self, hero, dt):
        if hero.actor.x < self.actor.x:
            self.direction = -1
            self.actor.x -= self.speed * 1.2
        else:
            self.direction = 1
            self.actor.x += self.speed * 1.2

    def _attack(self, hero, dt):
        """Start attack (only if cooldown is ready)."""
        if self._time_since_last_attack >= self.attack_cooldown:
            self._time_since_last_attack = 0.0
            self.is_attacking = True
            self.has_damaged = False
            self.frame_index = 0
            self._anim_timer = 0.0
            self._attack_timer = 0.0
            # Define a primeira frame de ataque
            if self.direction == -1:
                self.actor._surf = self.flipped_attack_frames[self.attack_frames[0]]
            else:
                self.actor.image = self.attack_frames[0]

    def _animate_attack(self, dt, hero):
        """Perform attack animation frame by frame."""
        self._anim_timer += dt

        if self._anim_timer >= self.frame_delay:
            self._anim_timer = 0.0
            self.frame_index += 1

            if self.frame_index < len(self.attack_frames):
                if self.direction == -1:
                    self.actor._surf = self.flipped_attack_frames[self.attack_frames[self.frame_index]]
                else:
                    self.actor.image = self.attack_frames[self.frame_index]
            else:
                # fim da animação
                self.is_attacking = False
                self.state = "patrol"
                self.frame_index = 0
                return

    # apply damage roughly in the middle of the animation
        if not self.has_damaged and 2 < self.frame_index < 4:
            dx = abs(self.actor.x - hero.actor.x)
            dy = abs(self.actor.y - hero.actor.y)
            if dx <= self.attack_range and dy < 50:
                try:
                    hero.take_damage(self.attack_damage)
                    self.has_damaged = True  # impede dano duplo
                except Exception:
                    pass

    # -------------------------------
    # ANIMAÇÕES ESPECÍFICAS
    # -------------------------------
    def _animate_idle(self, dt):
        """Animate idle state."""
        self._anim_timer += dt
        if self._anim_timer >= self.frame_delay:
            self._anim_timer = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.idle_frames)
            if self.direction == -1:
                self.actor._surf = self.flipped_idle_frames[self.idle_frames[self.frame_index]]
            else:
                self.actor.image = self.idle_frames[self.frame_index]

    def _animate_run(self, dt):
        """Animate running state."""
        self._anim_timer += dt
        if self._anim_timer >= self.frame_delay:
            self._anim_timer = 0.0
            self.frame_index = (self.frame_index + 1) % len(self.run_frames)
            if self.direction == -1:
                self.actor._surf = self.flipped_run_frames[self.run_frames[self.frame_index]]
            else:
                self.actor.image = self.run_frames[self.frame_index]

    def _apply_directioned_image(self):
        """Apply the correct image based on direction and state."""
        if self.state == "chase":
            frames = self.run_frames
            flipped_cache = self.flipped_run_frames
        else:
            frames = self.idle_frames
            flipped_cache = self.flipped_idle_frames
        
        idx = self.frame_index % len(frames)
        if self.direction == -1:
            self.actor._surf = flipped_cache[frames[idx]]
        else:
            self.actor.image = frames[idx]

    # -------------------------------
    # DEATH / DAMAGE
    # -------------------------------
    def take_damage(self, amount):
        if self.is_dead:
            return
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self._die()

    def _die(self):
        self.is_dead = True
        self.state = "dead"
        self.frame_index = 0
        self._anim_timer = 0.0
        if self.direction == -1:
            self.actor._surf = self.flipped_death_frames[self.death_frames[0]]
        else:
            self.actor.image = self.death_frames[0]

    def _update_death(self, dt):
        self._anim_timer += dt
        if self.frame_index < len(self.death_frames) - 1:
            if self._anim_timer >= self.frame_delay:
                self._anim_timer = 0
                self.frame_index += 1
                if self.direction == -1:
                    self.actor._surf = self.flipped_death_frames[self.death_frames[self.frame_index]]
                else:
                    self.actor.image = self.death_frames[self.frame_index]

    def bounding_box(self):
        return Rect(
            self.actor.left, self.actor.top, self.actor.width, self.actor.height
        )