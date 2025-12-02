import turtle
import random
import math

# ========================
# GAME SETUP
# ========================
screen = turtle.Screen()
screen.title("Space Invaders - Turtle Edition")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# ========================
# GAME VARIABLES
# ========================
score = 0
lives = 3
game_over = False
level = 1

enemy_speed = 1.0          # smoother movement
player_speed = 20
bullet_speed = 7
enemy_bullet_speed = 4

# ========================
# PLAYER
# ========================
player = turtle.Turtle()
player.shape("triangle")
player.color("cyan")
player.shapesize(stretch_wid=1, stretch_len=1.5)
player.penup()
player.goto(0, -250)
player.setheading(90)

# Lives display
lives_icons = []
for i in range(3):
    life = turtle.Turtle()
    life.shape("triangle")
    life.color("cyan")
    life.shapesize(0.5)
    life.penup()
    life.goto(-360 + i * 25, 260)
    life.setheading(90)
    lives_icons.append(life)

# ========================
# ENEMIES
# ========================
enemies = []
enemy_colors = ["red", "orange", "yellow", "green", "purple"]

def create_enemies():
    for row in range(4):
        for col in range(10):
            enemy = turtle.Turtle()
            enemy.shape("circle")
            enemy.color(random.choice(enemy_colors))
            enemy.penup()
            enemy.goto(-340 + col * 70, 200 - row * 50)
            enemy.dx = enemy_speed
            enemies.append(enemy)

create_enemies()

# ========================
# BULLETS
# ========================
bullets = []
max_bullets = 3

def shoot():
    if len(bullets) < max_bullets and not game_over:
        b = turtle.Turtle()
        b.shape("square")
        b.color("yellow")
        b.shapesize(0.2, 0.5)
        b.penup()
        b.goto(player.xcor(), player.ycor() + 20)
        b.setheading(90)
        bullets.append(b)

# Enemy bullets
enemy_bullets = []

def enemy_shoot():
    if enemies and random.random() < 0.02:
        shooter = random.choice(enemies)
        b = turtle.Turtle()
        b.shape("square")
        b.color("red")
        b.shapesize(0.2, 0.5)
        b.penup()
        b.goto(shooter.xcor(), shooter.ycor() - 15)
        b.setheading(270)
        enemy_bullets.append(b)

# ========================
# DISPLAYS
# ========================
score_display = turtle.Turtle()
score_display.hideturtle()
score_display.penup()
score_display.color("white")
score_display.goto(0, 260)

level_display = turtle.Turtle()
level_display.hideturtle()
level_display.penup()
level_display.color("white")
level_display.goto(320, 260)

def update_display():
    score_display.clear()
    level_display.clear()

    score_display.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))
    level_display.write(f"Lvl {level}", align="center", font=("Courier", 22, "normal"))

    for i, icon in enumerate(lives_icons):
        icon.hideturtle()
        if i < lives:
            icon.showturtle()

update_display()

# ========================
# CONTROLS
# ========================
def move_left():
    if not game_over:
        x = max(player.xcor() - player_speed, -360)
        player.setx(x)

def move_right():
    if not game_over:
        x = min(player.xcor() + player_speed, 360)
        player.setx(x)

def restart_game():
    global score, lives, game_over, level, enemies, bullets, enemy_bullets

    score = 0
    lives = 3
    game_over = False
    level = 1

    for e in enemies:
        e.hideturtle()
    for b in bullets + enemy_bullets:
        b.hideturtle()

    enemies.clear()
    bullets.clear()
    enemy_bullets.clear()

    player.goto(0, -250)
    create_enemies()
    update_display()

screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(shoot, "space")
screen.onkeypress(restart_game, "r")

# ========================
# COLLISION
# ========================
def collide(a, b, dist=20):
    return a.distance(b) < dist

# ========================
# GAME OVER DISPLAY
# ========================
game_over_text = turtle.Turtle()
game_over_text.hideturtle()
game_over_text.color("red")
game_over_text.penup()
game_over_text.goto(0, 0)

def show_game_over():
    global game_over
    game_over = True
    game_over_text.write("GAME OVER\nPress R to Restart",
                         align="center", font=("Courier", 34, "normal"))

# ========================
# GAME LOOP
# ========================
def game_loop():
    global score, lives, level, enemy_speed

    if not game_over:

        # Move enemies
        move_down = False
        for e in enemies:
            e.setx(e.xcor() + e.dx)

            if abs(e.xcor()) > 360:
                move_down = True

            if e.ycor() < -230:
                lives -= 1
                update_display()
                e.hideturtle()
                enemies.remove(e)
                if lives == 0:
                    show_game_over()
                    return

        if move_down:
            for e in enemies:
                e.sety(e.ycor() - 20)
                e.dx *= -1

        # Player bullets
        for b in bullets[:]:
            b.sety(b.ycor() + bullet_speed)

            if b.ycor() > 300:
                b.hideturtle()
                bullets.remove(b)
                continue

            for e in enemies[:]:
                if collide(b, e):
                    b.hideturtle()
                    e.hideturtle()
                    bullets.remove(b)
                    enemies.remove(e)
                    score += 10
                    update_display()
                    break

        # Enemy bullets
        enemy_shoot()

        for b in enemy_bullets[:]:
            b.sety(b.ycor() - enemy_bullet_speed)

            if b.ycor() < -300:
                b.hideturtle()
                enemy_bullets.remove(b)
                continue

            if collide(b, player, 25):
                b.hideturtle()
                enemy_bullets.remove(b)
                lives -= 1
                player.color("red")
                screen.ontimer(lambda: player.color("cyan"), 150)
                update_display()

                if lives == 0:
                    show_game_over()
                    return

        # Level up
        if len(enemies) == 0:
            level += 1
            enemy_speed *= 1.15
            create_enemies()
            update_display()

    screen.update()
    screen.ontimer(game_loop, 16)  # Smooth 60 FPS

# Start
game_loop()
turtle.mainloop()