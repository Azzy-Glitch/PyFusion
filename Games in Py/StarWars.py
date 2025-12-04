"""
Space Invaders - Enhanced Turtle Edition
Features included:
- Smooth movement and game loop (~60 FPS)
- Controls: Arrow keys + WASD, Space to shoot, P to pause, R to restart, M to mute
- Power-ups: Life, Rapid Fire, Piercing bullets
- Boss appears on Level 6 with HP and special behaviors
- Explosion effect using one turtle (no spam)
- Sound support on Windows via winsound (optional)
- Menu and pause screen
- Leaderboard saved to leaderboard.txt
- Optional sprite support — register GIFs and place them next to this script
"""

import turtle
import random
import math
import time
import json
import os

# Attempt to import winsound (Windows). If not available, sound functions will be no-ops.
try:
    import winsound
    SOUND_AVAILABLE = True
except Exception:
    SOUND_AVAILABLE = False

# -------------------------
# Configuration variables
# -------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TICK = int(1000 / FPS)

PLAYER_SPEED = 18
BULLET_SPEED = 10
ENEMY_BULLET_SPEED = 4.5
ENEMY_BASE_SPEED = 0.6
MAX_PLAYER_BULLETS = 3
POWERUP_CHANCE = 0.15
POWERUP_FALL_SPEED = 3
POWERUP_DURATION = 8.0  # seconds

BOSS_SPAWN_LEVEL = 6
BOSS_HP_BASE = 18

LEADERBOARD_FILE = "leaderboard.txt"
MAX_LEADERBOARD = 5

# -------------------------
# Initialize game objects
# -------------------------
screen = turtle.Screen()
screen.title("Space Invaders — Enhanced")
screen.bgcolor("black")
screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
screen.tracer(0)

# Global game state variables
game_state = "menu"  # menu, playing, paused, game_over, help, leaderboard
score = 0
lives = 3
level = 1
enemy_speed = ENEMY_BASE_SPEED
muted = False
rapid_fire_end_time = 0
piercing_end_time = 0

# Game object collections
enemies = []
player_bullets = []
enemy_bullets = []
powerups = []   # each powerup is dict {turtle, type}
explosions = []  # used for managing visual explosion lifecycle
boss = None
boss_hp = 0

# Timers
last_shot_time = 0
shot_cooldown = 0.28  # seconds normal
last_enemy_shot_global = 0

# Border turtle (persistent)
border_turtle = None

# -------------------------
# Utility / Sound functions
# -------------------------
def play_sound(sound_name):
    """Play simple sounds on Windows; no-op on other OSes."""
    if muted:
        return
    if not SOUND_AVAILABLE:
        return
    sounds = {
        "shoot": "shoot.wav",
        "explode": "explode.wav",
        "powerup": "powerup.wav",
        "boss": "boss.wav",
    }
    filename = sounds.get(sound_name)
    if filename and os.path.exists(filename):
        try:
            winsound.PlaySound(filename, winsound.SND_ASYNC)
        except Exception:
            pass

# -------------------------
# HUD Setup
# -------------------------
score_t = turtle.Turtle()
score_t.hideturtle()
score_t.penup()
score_t.color("lime")
score_t.goto(-350, SCREEN_HEIGHT//2 - 40)

level_t = turtle.Turtle()
level_t.hideturtle()
level_t.penup()
level_t.color("cyan")
level_t.goto(0, SCREEN_HEIGHT//2 - 40)

lives_t = turtle.Turtle()
lives_t.hideturtle()
lives_t.penup()
lives_t.color("yellow")
lives_t.goto(250, SCREEN_HEIGHT//2 - 40)

def update_hud():
    score_t.clear()
    level_t.clear()
    lives_t.clear()
    score_t.write(f"Score: {score}", align="left", font=("Courier", 18, "bold"))
    level_t.write(f"Level: {level}", align="center", font=("Courier", 18, "bold"))
    lives_t.write(f"Lives: {lives}", align="right", font=("Courier", 18, "bold"))

update_hud()

# -------------------------
# Player Setup
# -------------------------
player = turtle.Turtle()
player.shape("triangle")
player.color("cyan")
player.penup()
player.goto(0, -SCREEN_HEIGHT//2 + 60)
player.setheading(90)
player.shapesize(stretch_wid=1.2, stretch_len=1.2)  # Slightly larger player

# -------------------------
# Menu / UI Setup
# -------------------------
menu_turtle = turtle.Turtle()
menu_turtle.hideturtle()
menu_turtle.penup()
menu_turtle.color("white")

pause_turtle = turtle.Turtle()
pause_turtle.hideturtle()
pause_turtle.penup()
pause_turtle.color("yellow")

game_over_turtle = turtle.Turtle()
game_over_turtle.hideturtle()
game_over_turtle.penup()
game_over_turtle.color("red")

instructions_t = turtle.Turtle()
instructions_t.hideturtle()
instructions_t.penup()
instructions_t.color("white")
instructions_t.goto(0, -SCREEN_HEIGHT//2 + 30)

def draw_border():
    """Draw a decorative border that stays on screen"""
    global border_turtle
    if border_turtle:
        border_turtle.clear()
        border_turtle.hideturtle()
    
    border_turtle = turtle.Turtle()
    border_turtle.hideturtle()
    border_turtle.penup()
    border_turtle.color("cyan")
    border_turtle.pensize(3)
    border_turtle.goto(-SCREEN_WIDTH//2 + 50, SCREEN_HEIGHT//2 - 50)
    border_turtle.pendown()
    for _ in range(2):
        border_turtle.forward(SCREEN_WIDTH - 100)
        border_turtle.right(90)
        border_turtle.forward(SCREEN_HEIGHT - 100)
        border_turtle.right(90)
    border_turtle.penup()

def show_main_menu():
    global game_state, border_turtle
    game_state = "menu"
    clear_game_objects()
    menu_turtle.clear()
    pause_turtle.clear()
    game_over_turtle.clear()
    instructions_t.clear()
    
    # Draw border once
    draw_border()
    
    menu_turtle.goto(0, 100)
    menu_turtle.write("SPACE INVADERS", align="center", font=("Courier", 36, "bold"))
    menu_turtle.goto(0, 60)
    menu_turtle.write("ENHANCED EDITION", align="center", font=("Courier", 24, "bold"))
    menu_turtle.goto(0, 0)
    menu_turtle.write("Press ENTER to Start", align="center", font=("Courier", 22, "normal"))
    menu_turtle.goto(0, -40)
    menu_turtle.write("Press H for Help", align="center", font=("Courier", 18, "normal"))
    menu_turtle.goto(0, -80)
    menu_turtle.write("Press L to View Leaderboard", align="center", font=("Courier", 18, "normal"))
    
    instructions_t.goto(0, -SCREEN_HEIGHT//2 + 30)
    instructions_t.write("Controls: ←/→ or A/D to move | SPACE to shoot | P pause | R restart | M mute | ESC menu", 
                        align="center", font=("Courier", 12, "normal"))
    
    player.showturtle()
    player.goto(0, -SCREEN_HEIGHT//2 + 60)
    player.color("cyan")
    update_hud()
    screen.update()

def show_help():
    global game_state
    game_state = "help"
    menu_turtle.clear()
    instructions_t.clear()
    
    menu_turtle.goto(0, 140)
    menu_turtle.write("HOW TO PLAY", align="center", font=("Courier", 28, "bold"))
    menu_turtle.goto(0, 90)
    menu_turtle.write("Objective: Destroy all enemies. Avoid bullets.", align="center", font=("Courier", 16, "normal"))
    menu_turtle.goto(0, 60)
    menu_turtle.write("Power-ups:", align="center", font=("Courier", 18, "bold"))
    menu_turtle.goto(0, 30)
    menu_turtle.write("Life (green) - +1 Life", align="center", font=("Courier", 14, "normal"))
    menu_turtle.goto(0, 0)
    menu_turtle.write("Rapid-fire (blue) - Faster shooting", align="center", font=("Courier", 14, "normal"))
    menu_turtle.goto(0, -30)
    menu_turtle.write("Piercing (gold) - Bullets pierce enemies", align="center", font=("Courier", 14, "normal"))
    menu_turtle.goto(0, -70)
    menu_turtle.write("Controls: Arrow/A-D to move. Space to shoot.", align="center", font=("Courier", 14, "normal"))
    menu_turtle.goto(0, -100)
    menu_turtle.write("P to pause. R to restart. M to mute. ESC for menu.", align="center", font=("Courier", 14, "normal"))
    menu_turtle.goto(0, -150)
    menu_turtle.write("Press ESC to Return to Menu", align="center", font=("Courier", 16, "bold"))
    
    screen.update()

def show_leaderboard():
    global game_state
    game_state = "leaderboard"
    menu_turtle.clear()
    instructions_t.clear()
    
    menu_turtle.goto(0, 140)
    menu_turtle.write("LEADERBOARD", align="center", font=("Courier", 28, "bold"))
    top = load_leaderboard()
    menu_turtle.goto(0, 80)
    if not top:
        menu_turtle.write("No high scores yet.", align="center", font=("Courier", 16, "normal"))
    else:
        y = 70
        for i, item in enumerate(top, start=1):
            menu_turtle.goto(0, y)
            color = "gold" if i == 1 else "silver" if i == 2 else "#CD7F32" if i == 3 else "white"
            menu_turtle.color(color)
            menu_turtle.write(f"{i}. {item['name']} - {item['score']}", align="center", font=("Courier", 16, "normal"))
            y -= 30
    menu_turtle.color("white")
    menu_turtle.goto(0, -140)
    menu_turtle.write("Press ESC to return to menu", align="center", font=("Courier", 14, "bold"))
    
    screen.update()

# -------------------------
# Leaderboard functions
# -------------------------
def load_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception:
        pass
    return []

def save_score_to_leaderboard(name, sc):
    top = load_leaderboard()
    top.append({"name": name, "score": sc})
    top = sorted(top, key=lambda x: x["score"], reverse=True)[:MAX_LEADERBOARD]
    try:
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(top, f, indent=2)
    except Exception:
        pass

# -------------------------
# Game object management
# -------------------------
def clear_game_objects():
    """Clear all game objects from screen"""
    for e in enemies:
        try:
            e.hideturtle()
        except:
            pass
    enemies.clear()
    
    for b in player_bullets:
        try:
            b.hideturtle()
        except:
            pass
    player_bullets.clear()
    
    for b in enemy_bullets:
        try:
            b.hideturtle()
        except:
            pass
    enemy_bullets.clear()
    
    for p in powerups:
        try:
            p["t"].hideturtle()
        except:
            pass
    powerups.clear()
    
    for ex in explosions:
        try:
            ex["t"].hideturtle()
        except:
            pass
    explosions.clear()
    
    global boss
    if boss is not None:
        try:
            boss.hideturtle()
        except:
            pass
        boss = None

# -------------------------
# Enemy creation with border limits
# -------------------------
def create_enemies(rows=4, cols=10):
    global enemies, enemy_speed
    clear_game_objects()  # Clear existing enemies
    
    # Calculate starting position within border
    border_left = -SCREEN_WIDTH//2 + 70
    border_right = SCREEN_WIDTH//2 - 70
    border_top = SCREEN_HEIGHT//2 - 70
    
    available_width = border_right - border_left
    col_spacing = min(70, available_width / max(cols, 1))
    
    start_x = border_left + (available_width - (cols-1) * col_spacing) / 2
    start_y = border_top - 60
    
    for r in range(rows):
        for c in range(cols):
            e = turtle.Turtle()
            e.penup()
            e.shape("circle")
            colors = ["red", "orange", "yellow", "green", "purple"]
            e.color(colors[r % len(colors)])
            e.shapesize(stretch_wid=1.2, stretch_len=1.2)
            e.goto(start_x + c*col_spacing, start_y - r*48)
            e.dx = enemy_speed * (1 + 0.1 * (level - 1))
            enemies.append(e)

# -------------------------
# Boss spawn
# -------------------------
def spawn_boss():
    global boss, boss_hp
    boss = turtle.Turtle()
    boss.penup()
    boss.shape("square")
    boss.shapesize(stretch_wid=3, stretch_len=6)
    boss.color("purple")
    boss.goto(0, SCREEN_HEIGHT//2 - 120)
    boss.dx = 3.0 + level * 0.2
    boss_hp = BOSS_HP_BASE + (level - 1) * 4
    if SOUND_AVAILABLE:
        play_sound("boss")

# -------------------------
# Power-ups
# -------------------------
def maybe_drop_powerup(x, y):
    if random.random() < POWERUP_CHANCE:
        p = turtle.Turtle()
        p.penup()
        typ = random.choice(["life", "rapid", "pierce"])
        if typ == "life":
            p.shape("triangle"); p.color("green"); p.shapesize(stretch_wid=0.8, stretch_len=0.8)
        elif typ == "rapid":
            p.shape("square"); p.color("blue"); p.shapesize(stretch_wid=0.8, stretch_len=0.8)
        else:
            p.shape("circle"); p.color("gold"); p.shapesize(stretch_wid=0.8, stretch_len=0.8)
        p.goto(x, y)
        powerups.append({"t": p, "type": typ})

def apply_powerup(typ):
    global lives, rapid_fire_end_time, piercing_end_time
    play_sound("powerup")
    if typ == "life":
        lives += 1
        update_hud()
    elif typ == "rapid":
        rapid_fire_end_time = time.time() + POWERUP_DURATION
    elif typ == "pierce":
        piercing_end_time = time.time() + POWERUP_DURATION

# -------------------------
# Shooting
# -------------------------
def player_can_shoot():
    global last_shot_time
    cooldown = 0.12 if time.time() < rapid_fire_end_time else shot_cooldown
    return (time.time() - last_shot_time) >= cooldown and len(player_bullets) < MAX_PLAYER_BULLETS

def player_shoot():
    global last_shot_time
    if game_state != "playing":
        return
    if not player_can_shoot():
        return
    last_shot_time = time.time()
    b = turtle.Turtle()
    b.penup()
    b.shape("square")
    b.shapesize(stretch_wid=0.2, stretch_len=0.8)
    b.color("yellow")
    if time.time() < piercing_end_time:
        b.color("gold")
    b.goto(player.xcor(), player.ycor() + 18)
    b.setheading(90)
    b.piercing = (time.time() < piercing_end_time)
    player_bullets.append(b)
    play_sound("shoot")

def enemy_shoot_random():
    global last_enemy_shot_global
    if game_state != "playing":
        return
    now = time.time()
    if now - last_enemy_shot_global < 0.14:
        return
    if enemies and random.random() < 0.025:
        shooter = random.choice(enemies)
        b = turtle.Turtle()
        b.penup()
        b.shape("square")
        b.shapesize(stretch_wid=0.2, stretch_len=0.8)
        b.color("red")
        b.goto(shooter.xcor(), shooter.ycor() - 12)
        b.setheading(270)
        enemy_bullets.append(b)
        last_enemy_shot_global = now

def boss_shoot():
    if game_state != "playing":
        return
    global boss
    if boss is not None and random.random() < 0.03:
        for offset in (-18, 0, 18):
            b = turtle.Turtle()
            b.penup()
            b.shape("square")
            b.shapesize(stretch_wid=0.2, stretch_len=0.8)
            b.color("red")
            b.goto(boss.xcor() + offset, boss.ycor() - 40)
            b.setheading(270)
            enemy_bullets.append(b)

# -------------------------
# Explosions
# -------------------------
def spawn_explosion(x, y):
    e = turtle.Turtle()
    e.hideturtle()
    e.penup()
    e.goto(x, y)
    e.color("yellow")
    e.showturtle()
    e.shape("circle")
    explosions.append({"t": e, "start": time.time(), "dur": 0.36})

# -------------------------
# Collisions
# -------------------------
def is_collision(a, b, thresh=20):
    return a.distance(b) < thresh

# -------------------------
# Controls - COMPLETELY REWRITTEN
# -------------------------
def move_left():
    if game_state != "playing":
        return
    x = player.xcor() - PLAYER_SPEED
    if x < -SCREEN_WIDTH//2 + 70:  # Stay within border
        x = -SCREEN_WIDTH//2 + 70
    player.setx(x)

def move_right():
    if game_state != "playing":
        return
    x = player.xcor() + PLAYER_SPEED
    if x > SCREEN_WIDTH//2 - 70:  # Stay within border
        x = SCREEN_WIDTH//2 - 70
    player.setx(x)

def toggle_pause():
    global game_state
    if game_state == "playing":
        game_state = "paused"
        pause_turtle.clear()
        pause_turtle.goto(0, 0)
        pause_turtle.write("PAUSED\nPress P to Resume", align="center", font=("Courier", 24, "bold"))
    elif game_state == "paused":
        game_state = "playing"
        pause_turtle.clear()

def restart_game():
    global score, lives, level, enemy_speed, rapid_fire_end_time, piercing_end_time
    global game_state, boss_hp, boss
    
    # Clear all turtles first
    clear_game_objects()
    menu_turtle.clear()
    pause_turtle.clear()
    game_over_turtle.clear()
    instructions_t.clear()
    
    # Reset game state
    game_state = "playing"
    score = 0
    lives = 3
    level = 1
    enemy_speed = ENEMY_BASE_SPEED
    rapid_fire_end_time = 0
    piercing_end_time = 0
    boss = None
    boss_hp = 0
    
    # Reset player
    player.goto(0, -SCREEN_HEIGHT//2 + 60)
    player.color("cyan")
    player.showturtle()
    
    # Update display
    update_hud()
    create_enemies()
    screen.update()

def toggle_mute():
    global muted
    muted = not muted
    # Show mute status
    status = turtle.Turtle()
    status.hideturtle()
    status.penup()
    status.color("yellow")
    status.goto(0, 0)
    status.write(f"MUTE: {'ON' if muted else 'OFF'}", align="center", font=("Courier", 20, "bold"))
    screen.update()
    screen.ontimer(lambda: status.clear(), 1000)

def start_game():
    if game_state == "menu":
        restart_game()

def return_to_menu():
    global game_state
    if game_state in ["help", "leaderboard", "paused", "game_over", "playing"]:
        show_main_menu()

def handle_esc():
    """Handle ESC key - works from any state"""
    if game_state == "menu":
        # Already in menu, do nothing or quit
        pass
    elif game_state in ["help", "leaderboard", "paused", "game_over", "playing"]:
        return_to_menu()

def handle_r():
    """Handle R key - restart from game over or playing state"""
    if game_state in ["playing", "paused", "game_over"]:
        restart_game()

# Keyboard bindings - REBIND EVERYTHING
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(move_left, "a")
screen.onkeypress(move_right, "d")
screen.onkeypress(player_shoot, "space")
screen.onkeypress(toggle_pause, "p")
screen.onkeypress(handle_r, "r")  # Use dedicated handler
screen.onkeypress(toggle_mute, "m")
screen.onkeypress(start_game, "Return")
screen.onkeypress(show_help, "h")
screen.onkeypress(show_leaderboard, "l")
screen.onkeypress(handle_esc, "Escape")  # Use dedicated handler
screen.onkeypress(handle_esc, "Escape")

# -------------------------
# Main game loop
# -------------------------
def game_tick():
    global score, lives, level, enemy_speed, boss_hp, game_state
    global boss
    
    if game_state == "playing":
        # 1) Move enemies with border limits
        move_down = False
        border_left = -SCREEN_WIDTH//2 + 70
        border_right = SCREEN_WIDTH//2 - 70
        
        for e in enemies:
            e.setx(e.xcor() + e.dx)
            if e.xcor() > border_right or e.xcor() < border_left:
                move_down = True
        
        if move_down:
            for e in enemies:
                e.sety(e.ycor() - 20)
                e.dx *= -1
        
        # 2) Enemy shooting
        enemy_shoot_random()
        
        # 3) Move player bullets with border limits
        border_top = SCREEN_HEIGHT//2 - 50
        
        for b in player_bullets[:]:
            b.sety(b.ycor() + BULLET_SPEED)
            if b.ycor() > border_top:
                b.hideturtle()
                player_bullets.remove(b)
                continue
            
            # Check boss collision
            if boss is not None and is_collision(b, boss, thresh=50):
                spawn_explosion(b.xcor(), b.ycor())
                play_sound("explode")
                boss_hp -= 1
                
                if not getattr(b, "piercing", False):
                    b.hideturtle()
                    player_bullets.remove(b)
                
                if boss_hp <= 0:
                    spawn_explosion(boss.xcor(), boss.ycor())
                    boss.hideturtle()
                    boss = None
                    score += 200
                    level += 1
                    enemy_speed *= 1.12
                    create_enemies()
                    update_hud()
                continue
            
            # Check enemy collisions
            enemy_hit = None
            for e in enemies[:]:
                if is_collision(b, e, thresh=18):
                    enemy_hit = e
                    break
            
            if enemy_hit:
                spawn_explosion(enemy_hit.xcor(), enemy_hit.ycor())
                play_sound("explode")
                maybe_drop_powerup(enemy_hit.xcor(), enemy_hit.ycor())
                enemy_hit.hideturtle()
                enemies.remove(enemy_hit)
                
                if not getattr(b, "piercing", False):
                    b.hideturtle()
                    player_bullets.remove(b)
                
                score += 10
                update_hud()
        
        # 4) Move enemy bullets with border limits
        border_bottom = -SCREEN_HEIGHT//2 + 50
        
        for b in enemy_bullets[:]:
            b.sety(b.ycor() - ENEMY_BULLET_SPEED)
            if b.ycor() < border_bottom:
                b.hideturtle()
                enemy_bullets.remove(b)
                continue
            
            if is_collision(b, player, thresh=22):
                b.hideturtle()
                enemy_bullets.remove(b)
                lives -= 1
                update_hud()
                
                # Flash player
                player.color("red")
                def reset_color():
                    if player:
                        player.color("cyan")
                screen.ontimer(reset_color, 140)
                
                if lives <= 0:
                    game_state = "game_over"
                    # Clear everything except border
                    player.hideturtle()
                    clear_game_objects()
                    
                    # Show game over
                    game_over_turtle.clear()
                    game_over_turtle.goto(0, 50)
                    game_over_turtle.write("GAME OVER", align="center", font=("Courier", 48, "bold"))
                    game_over_turtle.goto(0, -20)
                    game_over_turtle.write(f"Final Score: {score}", align="center", font=("Courier", 24, "normal"))
                    game_over_turtle.goto(0, -60)
                    game_over_turtle.write("Press R to Restart | ESC for Menu", 
                                          align="center", font=("Courier", 16, "normal"))
                    
                    # Save to leaderboard
                    screen.update()
                    screen.ontimer(lambda: ask_for_leaderboard_name(score), 500)
        
        # 5) Move powerups with border limits
        for p in powerups[:]:
            p["t"].sety(p["t"].ycor() - POWERUP_FALL_SPEED)
            if p["t"].ycor() < border_bottom:
                p["t"].hideturtle()
                powerups.remove(p)
                continue
            
            if is_collision(p["t"], player, thresh=18):
                apply_powerup(p["type"])
                p["t"].hideturtle()
                powerups.remove(p)
        
        # 6) Boss logic with border limits
        if boss is not None:
            boss_left_limit = -SCREEN_WIDTH//2 + 150
            boss_right_limit = SCREEN_WIDTH//2 - 150
            
            boss.setx(boss.xcor() + boss.dx)
            if boss.xcor() > boss_right_limit or boss.xcor() < boss_left_limit:
                boss.dx *= -1
            boss_shoot()
        
        # 7) Explosion animations
        for ex in explosions[:]:
            elapsed = time.time() - ex["start"]
            frac = elapsed / ex["dur"]
            if frac >= 1.0:
                ex["t"].hideturtle()
                explosions.remove(ex)
            else:
                size = 1 + frac * 2.8
                ex["t"].shapesize(size, size)
                # Change color during explosion
                if frac < 0.33:
                    ex["t"].color("yellow")
                elif frac < 0.66:
                    ex["t"].color("orange")
                else:
                    ex["t"].color("red")
        
        # 8) Level progression
        if not enemies and boss is None:
            if level % BOSS_SPAWN_LEVEL == 0:
                spawn_boss()
            else:
                level += 1
                enemy_speed *= 1.12
                rows = 4 + (level - 1) // 3
                cols = 8 + (level - 1) // 2
                create_enemies(rows=min(rows, 6), cols=min(cols, 12))
                update_hud()
        
        # 9) Show powerup status
        if time.time() < rapid_fire_end_time or time.time() < piercing_end_time:
            status_t = turtle.Turtle()
            status_t.hideturtle()
            status_t.penup()
            status_t.color("white")
            status_t.goto(0, -SCREEN_HEIGHT//2 + 100)
            status_str = ""
            if time.time() < rapid_fire_end_time:
                status_str += "RAPID FIRE "
            if time.time() < piercing_end_time:
                status_str += "PIERCING"
            status_t.write(status_str, align="center", font=("Courier", 12, "bold"))
            screen.ontimer(lambda: status_t.clear(), 50)
    
    # Update HUD
    update_hud()
    screen.update()
    screen.ontimer(game_tick, TICK)

def ask_for_leaderboard_name(final_score):
    """Ask for name after game over"""
    try:
        name = screen.textinput("Game Over", 
                               f"Your score: {final_score}\nEnter your name for leaderboard (leave empty to skip):")
        if name and name.strip():
            save_score_to_leaderboard(name.strip(), final_score)
    except Exception:
        pass  # Ignore textinput errors

# -------------------------
# Start the game
# -------------------------
show_main_menu()
screen.ontimer(game_tick, TICK)

try:
    turtle.mainloop()
except KeyboardInterrupt:
    print("\nGame closed by user")
except Exception as e:
    print(f"An error occurred: {e}")