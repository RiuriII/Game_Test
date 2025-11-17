# -*- coding: utf-8 -*-
# type: ignore
import pgzrun
from pygame import Rect
from modules.Hero import Hero
from modules.Enemy import Enemy
from modules.Platform import Platform

# game constants
WIDTH = 800
HEIGHT = 600
TITLE = "Platformer - Test Project"

# game variables
score = 0  # System score
SCORE_TO_WIN = 5  # Needed score to win
music_on = True
game_state = "menu" # menu, playing, gameover
gameover_timer = 0   # Counter for game over delay

# game UI elements
start_button = Rect((WIDTH // 2 -125, HEIGHT // 2), (250, 50))
back_menu_button = Rect((WIDTH // 2 -125, HEIGHT // 2 + 140), (250, 50))  # Position (200, 150), Size (100, 50)
sound_button = Rect((WIDTH // 2 -125, HEIGHT // 2 + 70), (250, 50))
exit_button = Rect((WIDTH // 2 -125, HEIGHT // 2 + 210) , (250, 50))

# game objects
sky = Actor("background", (WIDTH // 2, HEIGHT // 2))
hero = Hero(40, 400)

# Enemy list 
enemies = [Enemy(500, 515, patrol_width=140) for _ in range(5)]

# Reset hero position and state
def reset_hero():
    hero.actor.x = 40
    hero.actor.y = 400
    hero.vel_y = 0
    hero.is_dead = False
    hero.health = 100


platform_data = [
    Platform(100, 450, 150, 20, has_enemy=True),
    Platform(350, 380, 200, 20, has_enemy=True),
    Platform(600, 300, 150, 20, has_enemy=True),
    Platform(200, 250, 120, 20, has_enemy=False),
]

platforms = [plat.rect for plat in platform_data]


def spawn_all_enemies():
    """Create enemies on all platforms that should have them."""
    global enemies
    enemies = []
    
    # Spawn enemies on platforms
    for plat in platform_data:
        enemy = plat.spawn_enemy()
        if enemy:
            enemies.append(enemy)

spawn_all_enemies()
SCORE_TO_WIN = len(enemies) # Update score to win based on number of enemies

def update(dt):
    """
    Function called automatically to update the game state.
    'dt' is the time elapsed since the last call (in seconds).
    """
    screen.fill((0, 0, 0)) # Clear screen with black
    
    global game_state, gameover_timer

    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_game()
        hero.update(dt, platforms)
        for enemy in enemies:
            enemy.update(dt, hero)
        
        if  hero.is_dead:
            gameover_timer += dt
            if gameover_timer >= 1:  # 2s delay 
                game_state = "gameover"

        for proj in hero.projectiles:
             for enemy in enemies:
                if proj.alive and not enemy.is_dead and enemy.actor.colliderect(proj.rect):
                    enemy.take_damage(10)
                    proj.alive = False
                    
                    # Incrementa o score when enemy is dead
                    if enemy.is_dead:
                        global score
                        score += 1
                        
                        # Verify if player won
                        if score >= SCORE_TO_WIN:
                            game_state = "win"
                        

    elif game_state == "gameover":
        draw_gameover()
        reset_hero()

    elif game_state == "win":
            draw_victory()
            for enemy in enemies:
                enemy.health = 100
                enemy.is_dead = False 
                reset_hero()


def draw_menu():
    """
    Draws the main menu.
    """
    screen.fill((56,24,76))

  # Title
    screen.draw.text(
        "PLATFORMER GAME",
        center=(WIDTH/2, HEIGHT/2 - 100),
        color=(255, 255, 255),
        fontsize=60
    )

    screen.draw.filled_rect(start_button, (50, 200, 50))
    screen.draw.text("START GAME", center=start_button.center, fontsize=25, color=(255, 255, 255))
    
    sound_color = (50, 200, 50) if music_on else (200, 50, 50)
    screen.draw.filled_rect(sound_button, sound_color)
    screen.draw.text(f"SOUND: {'ON' if music_on else 'OFF'}", center=sound_button.center, fontsize=25, color=(255, 255, 255))
    
    screen.draw.filled_rect(back_menu_button, (50, 200, 50))
    screen.draw.text("Press M back to menu", center=back_menu_button.center, fontsize=25, color=(255, 255, 255))

    screen.draw.filled_rect(exit_button, (200, 50, 50))
    screen.draw.text("Exit", center=exit_button.center, fontsize=25, color=(255, 255, 255))


def draw_game():
    """
    Draws the main game screen.
    """
    # background
    sky.draw()
    # Character
    hero.draw(screen)
    for enemy in enemies:
        if not enemy.is_dead:
            enemy.draw()


    # Environment - Ground
    screen.draw.filled_rect(Rect(0,550,800,50), (109, 83, 166))

    # Platforms
    for plat in platforms:
            screen.draw.filled_rect(plat, (109, 83, 166))
            screen.draw.rect(plat, (109, 83, 166))

    # HUD
    draw_hud()


def draw_hud():
    """Draw heads-up display information."""
    screen.draw.text(f"Lives: {hero.health}", (10, 10), 
                    fontsize=30, color=(255, 255, 255))
    screen.draw.text(f"Score: {score}/{SCORE_TO_WIN}", (10, 50), 
                    fontsize=30, color=(255, 215, 0))
    
    enemies_alive = sum(not enemy.is_dead for enemy in enemies)
    screen.draw.text(f"Enemies: {enemies_alive}", (WIDTH - 150, 10), 
                    fontsize=25, color=(255, 100, 100))


def draw_gameover():
    """Game Over Screen."""
    screen.draw.text(
        "GAME OVER",
        center=(WIDTH/2, HEIGHT/2 - 50),
        color=(255, 0, 0),
        fontsize=80
    )
    screen.draw.text(
        f"Score: {score}",
        center=(WIDTH/2, HEIGHT/2 + 20),
        color=(255, 255, 255),
        fontsize=40
    )
    screen.draw.text(
        "Press ENTER to return to menu",
        center=(WIDTH/2, HEIGHT/2 + 50),
        color=(255, 255, 255),
        fontsize=30
    )


def draw_victory():
    """Victory Screen."""
    global score
    screen.draw.text(
        "YOU WIN!",
        center=(WIDTH/2, HEIGHT/2 - 50),
        color=(0, 255, 0),
        fontsize=80
    )
    screen.draw.text(
        f"Score: {score}/{SCORE_TO_WIN}",
        center=(WIDTH/2, HEIGHT/2 + 20),
        color=(255, 215, 0),
        fontsize=40
    )
    screen.draw.text(
        "Press ENTER to return to menu",
        center=(WIDTH/2, HEIGHT/2 + 50),
        color=(255, 255, 255),
        fontsize=30
    )



def on_key_down(key):
    """
    Function called automatically when a key is pressed.
    'key' is the key that was pressed.
    """
    global game_state

    if game_state == "menu":
        if key == keys.RETURN:
            game_state = "playing"
        elif key == keys.ESCAPE:
            exit() # Exit the game
            
    elif game_state == "playing":
        if key == keys.M:
            game_state = "menu"

    elif game_state == "gameover":
        global gameover_timer
        if key == keys.RETURN:
            game_state = "menu"
            hero.health = 100
            hero.is_dead = False
            gameover_timer = 0
    elif game_state == "win":
        if key == keys.RETURN:
            global score
            game_state = "menu"
            score = 0


def on_mouse_down(pos):
    """
    Function called automatically when a mouse button is pressed.
    'pos' is the (x, y) tuple of the click position.    
    """
    # Verify if click is on buttons
    global music_on
    if sound_button.collidepoint(pos):
        music_on = not music_on
        start_music()

    elif start_button.collidepoint(pos):
        global game_state
        game_state = "playing"

    elif exit_button.collidepoint(pos):
        exit()
            

    
def start_music():
    if music_on:
        try:
            music.play("background")
            music.set_volume(0.6)
        except Exception:
            pass
    else:
        music.stop()


start_music()

pgzrun.go()