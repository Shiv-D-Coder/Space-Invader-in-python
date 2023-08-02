import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()   # MUST USE TO START PYGAME
screen = pygame.display.set_mode((800, 600))

# Set window caption and icon
pygame.display.set_caption("Space Game")          # ADD CAPTION AND ICON
icon = pygame.image.load("img1.png")
pygame.display.set_icon(icon)

# Load and play background music
background = pygame.image.load("background.jpg")  
mixer.music.load("background_sound.mp3")
mixer.music.play(-1)

# Load player image and set initial coordinates and movement speed
playerImg = pygame.image.load("space_ship.png")
playerX = 370
playerY = 480
change_in_player_X = 0
chnage_in_player_Y = 0

# Load enemy images and set initial coordinates and movement speed for multiple enemies
enemyImg = []
enemyX = []
enemyY = []
change_in_enemy_X = []
chnage_in_enemy_Y = []
no_of_enemies = 6
 
for i in range(no_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png")) 
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(30, 180))
    change_in_enemy_X.append(0.3)
    chnage_in_enemy_Y.append(40)

# Load bullet image and set initial coordinates and movement speed
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
change_in_bullet_X = 0
chnage_in_bullet_Y = 3
bullet_state = "ready"

# Load font for displaying the score
score_value = 0
font = pygame.font.Font('freeshippingital.ttf',40)
scoreX = 10
scoreY = 10

# Load font for displaying "Game Over" text
over_font = pygame.font.Font('freeshippingital.ttf',75)

# Function to display "Game Over" text
def game_over():
    over_text = over_font.render("GAME OVER ", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

# Function to display the score
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (39, 244, 11))
    screen.blit(score, (x, y))

# Function to display the player image
def player(x, y):
    screen.blit(playerImg, (x, y))

# Function to display enemy images
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Function to fire bullets
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))    

# Function to check for collisions between bullet and enemy
def isCollision(cor_bulletX, cor_enemyX, cor_bulletY, cor_enemyY):  
    distance = math.sqrt((math.pow(cor_bulletX - cor_enemyX, 2)) + (math.pow(cor_bulletY - cor_enemyY, 2)))  
    if distance < 27:
        return True
    else:
        return False

# Main game loop
running = True
while running:
    # Event handling loop
    screen.fill((0, 0, 0))         # Set background color
    screen.blit(background, (0, 0))  # Add background image
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
             
        if event.type == pygame.KEYDOWN:  # Handle player movement and bullet firing
            if event.key == pygame.K_LEFT:
                change_in_player_X = -0.4  
            if event.key == pygame.K_RIGHT:
                change_in_player_X = 0.4 
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    fire_sound = mixer.Sound("shoot_sound.wav")
                    fire_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)  
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change_in_player_X = 0
                
    # Bound player movement within screen boundaries
    if playerX <= 0:
        playerX = 0
    if playerX >= 736:
        playerX = 736 
    playerX += change_in_player_X
               
    # Check for enemy collisions and game over condition
    for i in range(no_of_enemies):
        if enemyY[i] > 440:
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            game_over()
                
        if enemyX[i] <= 0:
            change_in_enemy_X[i] = 0.3 
            enemyY[i] += chnage_in_enemy_Y[i]
        if enemyX[i] >= 736:
            change_in_enemy_X[i] = -0.3  
            enemyY[i] += chnage_in_enemy_Y[i] 
        enemyX[i] += change_in_enemy_X[i] 
        
        # Check for collision between bullet and enemy
        collision = isCollision(bulletX, enemyX[i], bulletY, enemyY[i])
        if collision:
            explore_sound = mixer.Sound("explore_sound.wav")
            explore_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)   
            enemyY[i] = random.randint(30, 180)
        
        enemy(enemyX[i], enemyY[i], i)

    # Move bullet and fire bullets
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= chnage_in_bullet_Y   
    
    # Update player position and display score
    playerX += change_in_player_X
    player(playerX, playerY)
    show_score(scoreX, scoreY)
    pygame.display.update()

pygame.quit()
