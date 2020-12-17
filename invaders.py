import pygame
import os
import time
import random
from entities import Player, Enemy, collide

pygame.font.init()

COLOR_WHITE = (255,255,255)
COLOR_RED = (255,0,0)
COLOR_GREEN = (69, 252, 3)

GAME_WIDTH = 800
GAME_HEIGHT = 600
PLAYER_SPEED = 4
ENEMY_SPEED = 1
BULLET_SPEED = 5

SOLDIER = 'soldier'
CAPTAIN = 'captain'
BOSS = 'boss'

#WINDOW SETUP
WINDOW = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

#LOAD IMAGES
BACKGROUND = pygame.image.load(os.path.join("assets", "background.jpg"))
ENEMY_UFO = pygame.image.load(os.path.join("assets", "ufo.png"))
ENEMY_UFO_STRONG = pygame.image.load(os.path.join("assets", "ufo_stronger.png"))
ENEMY_UFO_BOSS = pygame.image.load(os.path.join("assets", "ufo_boss.png"))
PLAYER_SPACESHIP = pygame.image.load(os.path.join("assets", "player.png"))

def main():
    run = True
    pause = False
    FPS = 60
    level = 0
    lives = 5
    clock = pygame.time.Clock()

    main_font = pygame.font.Font(os.path.join("assets", "invaders.ttf"), 20)
    game_over_font = pygame.font.Font(os.path.join("assets", "invaders.ttf"), 28)
    player_x = int((GAME_WIDTH / 2) - (PLAYER_SPACESHIP.get_width() / 2))   #center player horizontally
    player_y = 480
    player = Player(player_x, player_y, PLAYER_SPACESHIP)

    enemies=[]
    wave_length = 5
    lost = False
    lost_count = 0

    def redraw_window():
        WINDOW.blit(BACKGROUND, (0,0))
        #text
        
        lives_label = main_font.render(f"Lives: {lives}", True , COLOR_WHITE)
        level_label = main_font.render(f"Level: {level}", True, COLOR_WHITE)

        WINDOW.blit(lives_label, (10, 10))
        level_label_x = GAME_WIDTH - level_label.get_width() - 10
        WINDOW.blit(level_label, (level_label_x, 10))

        #DRAW ENEMIES
        for enemy in enemies:
            enemy.draw(WINDOW)

        #DRAW PLAYER
        player.draw(WINDOW)

        if lost:
            game_over_label = game_over_font.render(f"GAME OVER", True , COLOR_RED)
            WINDOW.blit(game_over_label, ((GAME_WIDTH/2)-(game_over_label.get_width()/2), 
                                            (GAME_HEIGHT/2) - (game_over_label.get_height()/2)))

        if pause:
            pause_label= main_font.render("Game paused...", True , COLOR_WHITE)
            WINDOW.blit(pause_label, ((GAME_WIDTH/2)-(pause_label.get_width()/2), 
                                            (GAME_HEIGHT/2) - (pause_label.get_height()/2)))
            
        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window()

        #CHECK REMAINING LIVES
        if lives == 0:
            lost= True
            lost_count += 1

        #take life if health is depleted
        if player.health <= 0 and lives > 0:
            lives -= 1
            player.health = 100

        #SHOW GAME OVER MESSAGE FOR 3 SECS THEN QUIT
        if lost:
            if lost_count > FPS * 3:
                run= False
            else:
                continue
        

        #SEND WAVES OF ENEMIES
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(
                    random.randrange(50, GAME_WIDTH-64), #enemy sprite is 64x64 px
                    random.randrange(-1500, -100), 
                    random.choice([SOLDIER,CAPTAIN,BOSS]))
                enemies.append(enemy)

        #CHECK QUIT        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                quit()

        #CHECK PRESSED KEYS
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            #MOVE PLAYER LEFT
            if not player.boundary_left():
                player.move_left(PLAYER_SPEED)
            
        if keys[pygame.K_RIGHT]:
            #MOVE PLAYER RIGHT
            if not player.boundary_right(GAME_WIDTH):
                player.move_right(PLAYER_SPEED)

        if keys[pygame.K_DOWN]:
            #MOVE PLAYER DOWN
            if not player.boundary_down(GAME_HEIGHT):
                player.move_down(PLAYER_SPEED)

        if keys[pygame.K_UP]:
            #MOVE PLAYER UP
            if not player.boundary_up():
                player.move_up(PLAYER_SPEED)        

        if keys[pygame.K_SPACE]:  
            player.shoot()
        
        if keys[pygame.K_ESCAPE]:
            pause = not pause

        #pause menu
        if pause:
            continue
        
        #MOVE ENEMIES
        for enemy in enemies[:]:
            enemy.move_down(ENEMY_SPEED)
            enemy.move_lasers(BULLET_SPEED, GAME_HEIGHT, player)

            #enemy shooting chance
            if random.randrange(0, 2*60) == 1:              #enemy shooting probability
                enemy.shoot()

            #check collision between enemy and player
            if collide(enemy, player):
                player.health -= 50
                enemies.remove(enemy)
                #when enemy leaves the screen remove and take a life
            elif enemy.check_off_screen(GAME_HEIGHT):
                player.health -= 20
                enemies.remove(enemy)


        player.move_lasers(-BULLET_SPEED, GAME_HEIGHT, enemies)

def main_menu():
    run = True
    title_font = pygame.font.Font(os.path.join("assets", "invaders.ttf"), 60)
    subtitle_font = pygame.font.Font(os.path.join("assets", "invaders.ttf"), 20)
    while run:

        WINDOW.blit(BACKGROUND, (0,0))
        title_label = title_font.render("SPACE INVADERS", True, COLOR_WHITE)
        subtitle_label = subtitle_font.render("press SPACEBAR to begin...", True, COLOR_WHITE)
        WINDOW.blit(title_label, (GAME_WIDTH/2-title_label.get_width()/2, 100))
        WINDOW.blit(subtitle_label, (GAME_WIDTH/2-subtitle_label.get_width()/2, 480))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE]:
                main()

        pygame.display.update()

    pygame.quit()


main_menu()