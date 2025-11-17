# -*- coding: utf-8 -*-
# type: ignore
import pgzrun
from pgzero.builtins import Actor, keyboard, sounds
from pygame import Rect

from modules.Projectile import Projectile
from modules.Sprite import SpriteManager

class Hero:
    def __init__(self, x, y):
        self.actor = Actor("hero_idle1", (x, y))  # imagem inicial
        self.vel_y = 0
        self.on_ground = False
        self.speed = 4
        self.jump_strength = -15
        self.gravity = 0.8
        self.health = 100
        self.ground_y = 522
        self.direction = 1

        # States
        self.is_dead = False
        self.is_attacking = False

        # Animation control
        self.frame_index = 0
        self.frame_delay = 0.15
        self.time_since_last = 0
        self.idle_frames = ["hero_idle1", "hero_idle2", "hero_idle3"]
        self.death_frames = [
            "hero_death1", "hero_death2", "hero_death3",
            "hero_death4", "hero_death5", "hero_death6",
        ]
        self.attack_frames = [
            "hero_attack1", "hero_attack2", "hero_attack3",
            "hero_attack4", "hero_attack5", "hero_attack6",
            "hero_attack7",
        ]

        self.projectiles = []  # list of active projectiles
        self._has_shot = False  # control to avoid multiple shots during one attack

        self.flipped_attack_frames = SpriteManager.preload_flipped_frames(self.attack_frames)
        self.flipped_idle_frames = SpriteManager.preload_flipped_frames(self.idle_frames)
        self.flipped_death_frames = SpriteManager.preload_flipped_frames(self.death_frames)


    def update(self, dt, platforms, screen_width=800):
        """Update position and apply gravity."""
        if self.is_dead:
            self.animate_death(dt)
            return

        if self.is_attacking:
            self.animate_attack(dt)
            return

        self.apply_gravity(platforms)
        self.handle_input()
        self.animate_idle(dt)

        # atualiza projéteis
        for proj in self.projectiles:
            proj.update(screen_width)
        # remove projéteis mortos
        self.projectiles = [p for p in self.projectiles if p.alive]

    def draw(self, screen):
        """Draw the hero on the screen."""
        self.actor.draw()
        for proj in self.projectiles:
            proj.draw(screen)


    def apply_gravity(self, platforms):
        """Apply gravity and correct vertical collision."""
        self.vel_y += self.gravity
        self.actor.y += self.vel_y
        self.on_ground = False

        # Verifica colisão com o chão
        if self.actor.y >= self.ground_y:
            self.actor.y = self.ground_y
            self.vel_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        # Verifica colisão com plataformas
        for p in platforms:
            # Usa o método colliderect do próprio Actor!
            if self.actor.colliderect(p):
                # Colisão enquanto CAI (vel_y positivo)
                if self.vel_y > 0:
                    # Verifica se estava acima da plataforma
                    if self.actor.bottom - self.vel_y <= p.top + 5:
                        self.actor.bottom = p.top
                        self.vel_y = 0
                        self.on_ground = True
                        
                # Colisão enquanto SOBE (batendo a cabeça)
                elif self.vel_y < 0:
                    if self.actor.top >= p.bottom - 10:
                        self.actor.top = p.bottom
                        self.vel_y = 0

    def start_attack(self):
        """Start the attack (animation and state)."""
        self.is_attacking = True
        self.frame_index = 0
        self.time_since_last = 0
        # define a primeira frame de ataque imediatamente
        # self.actor.image = self.attack_frames[self.frame_index]
        if self.direction == -1:
            self.actor._surf = self.flipped_attack_frames[self.attack_frames[0]]
        else:
            self.actor.image = self.attack_frames[0]

    def handle_input(self):
        """Control lateral movement, jump, and start attack."""
        if keyboard.left:
            self.actor.x -= self.speed
            self.direction = -1
        elif keyboard.right:
            self.actor.x += self.speed
            self.direction = 1

        # Atualiza imagem conforme a direção (idle)
        if not self.is_attacking:
            if self.direction == -1:
                self.actor._surf = self.flipped_idle_frames[self.idle_frames[self.frame_index]]
            else:
                self.actor.image = self.idle_frames[self.frame_index]

        # pular
        if keyboard.SPACE and self.on_ground:
            self.vel_y = self.jump_strength
            self.on_ground = False
            sounds.jump.play()

        # attack: start only once when the key is pressed
        # (assumes handle_input runs every frame; start_attack is only called if not already attacking)
        if keyboard.Z and not self.is_attacking and self.on_ground:
            self.start_attack()
            sounds.attack.play()

    def animate_idle(self, dt):
        """Anima o personagem parado (loop)."""
        self.time_since_last += dt
        if self.time_since_last >= self.frame_delay:
            self.time_since_last = 0
            self.frame_index = (self.frame_index + 1) % len(self.idle_frames)
            if self.direction == -1:
                self.actor._surf = self.flipped_idle_frames[self.idle_frames[self.frame_index]]
            else:
                self.actor.image = self.idle_frames[self.frame_index]

    def animate_attack(self, dt):
        """Anima o ataque frame a frame; termina e volta ao idle."""
        self.time_since_last += dt
        if self.time_since_last >= self.frame_delay:
            self.time_since_last = 0
            self.frame_index += 1

            if self.frame_index < len(self.attack_frames):

                if self.direction == -1:
                    # Usa a surface flipada do cache
                    self.actor._surf = self.flipped_attack_frames[self.attack_frames[self.frame_index]]
                else:
                    self.actor.image = self.attack_frames[self.frame_index]

                # dispara o projétil em um frame específico (ex: frame 3)
                if self.frame_index == 3 and not self._has_shot:
                    self.shoot_projectile()
                    self._has_shot = True

            else:
                # terminou a animação de ataque
                self.is_attacking = False
                self.frame_index = 0
                self.time_since_last = 0
                self._has_shot = False
                # volta para frame idle inicial
                if self.direction == -1:
                    self.actor._surf = self.flipped_idle_frames[self.idle_frames[0]]
                else:
                    self.actor.image = self.idle_frames[0]

    def animate_death(self, dt):
        """Animation of death (can loop or advance as needed)."""
        self.time_since_last += dt
        if self.time_since_last >= self.frame_delay:
            self.time_since_last = 0
            self.frame_index = (self.frame_index + 1) % len(self.death_frames)
            if self.direction == -1:
                self.actor._surf = self.flipped_death_frames[self.death_frames[self.frame_index]]
            else:
                self.actor.image = self.death_frames[self.frame_index]

    def take_damage(self, amount):
        """Aplica dano e verifica morte."""
        if not self.is_dead:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.is_dead = True
                self.frame_index = 0
                self.time_since_last = 0
                self.actor.image = self.death_frames[0]

    def shoot_projectile(self):
        """Cria e adiciona um novo projétil à lista."""
        offset_x = 15 * self.direction
        new_proj = Projectile(self.actor.x + offset_x, self.actor.y - 2, self.direction)
        self.projectiles.append(new_proj)

