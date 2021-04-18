import pygame
import math
import random
from pygame import mixer

# intialize the pygame
pygame.init()

# create the game window
screen = pygame.display.set_mode((800, 600))
# BackGround Music
# Title and  Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("001-ufo.png")
pygame.display.set_icon(icon)

# Background image
background_img = pygame.image.load("background.jpg")
# Players
playerImg = pygame.image.load("space.png")
playerx = 370
playery = 480
playerx_change = 0

# Enemy
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
number_of_enemy = 6
for i in range(number_of_enemy):
    EnemyImg.append(pygame.image.load("001-ufo.png"))
    EnemyX.append(random.randint(0, 735))
    EnemyY.append(random.randint(50, 150))
    EnemyX_change.append(0.3)
    EnemyY_change.append(40)

# Bullet
BulletImg = pygame.image.load("bullet.png")
BulletX = 0
BulletY = 480
BulletX_change = 0
BulletY_change = 2.5
# ready means You can not see the bullet on the screen
# Fire the bullet is currently moving
Bullet_State = "ready"

# Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10

# Game over
over_font = pygame.font.Font("freesansbold.ttf", 80)


def score_shoe(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def Enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))


def Fire_bullet(x, y):
    global Bullet_State
    Bullet_State = "fire"
    screen.blit(BulletImg, (x + 16, y + 10))


def isCollision(EnemyX, EnemyY, BulletX, BulletY):
    distance = math.sqrt(math.pow(EnemyX - BulletX, 2) + math.pow(BulletY - EnemyY, 2))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:
    # RGB Red blue green
    screen.fill((0, 255, 255))
    # background image
    screen.blit(background_img, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is prassed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.4
            if event.key == pygame.K_SPACE:
                if Bullet_State is "ready":
                    bullet_sound = mixer.Sound("Laser.wav")
                    bullet_sound.play()
                    BulletX = playerx
                    Fire_bullet(BulletX, BulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
    # checking for boundries
    playerx += playerx_change

    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736
    for i in range(number_of_enemy):
        # Game Over
        if EnemyY[i] > 440:
            for j in range(number_of_enemy):
                EnemyY[j] = 2000
            game_over_text()
            break
        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <= 0:
            EnemyX_change[i] = 0.3
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 768:
            EnemyX_change[i] = -0.3
            EnemyY[i] += EnemyY_change[i]
        # Collisison of bullet
        collision = isCollision(EnemyX[i], EnemyY[i], BulletX, BulletY)
        if collision:
            collision_sound = mixer.Sound("Explosion.wav")
            collision_sound.play()
            BulletY = 480
            Bullet_State = "ready"
            score_value += 1
            EnemyX[i] = random.randint(0, 735)
            EnemyY[i] = random.randint(50, 150)
        Enemy(EnemyX[i], EnemyY[i], i)
    # Bullet Movement
    if BulletY <= 0:
        BulletY = 480
        Bullet_State = "ready"

    if Bullet_State is "fire":
        Fire_bullet(BulletX, BulletY)
        BulletY -= BulletY_change

    player(playerx, playery)
    score_shoe(textX, textY)
    pygame.display.update()
