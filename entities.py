import pygame
import os

ENEMY_UFO = pygame.image.load(os.path.join("assets", "ufo.png"))
ENEMY_UFO_STRONG = pygame.image.load(os.path.join("assets", "ufo_stronger.png"))
ENEMY_UFO_BOSS = pygame.image.load(os.path.join("assets", "ufo_boss.png"))

UFO_HEALTH = 100
UFO_STRONGER_HEALTH = 150
BOSS_HEALTH = 300

UFO_POINTS = 10
UFO_STRONGER_POINTS = 30
UFO_BOSS_POINTS = 50

PLAYER_BULLET = pygame.image.load(os.path.join("assets", "missile.png"))
ENEMY_BULLET = pygame.image.load(os.path.join("assets", "bomb.png"))

COLOR_RED = (255,0,0)
COLOR_GREEN = (69, 252, 3)

def collide(object, other_object):
        offset_x = object.x - other_object.x
        offset_y = object.y - other_object.y
        return (object.mask.overlap(other_object.mask, (offset_x, offset_y)) != None)

class Ship:
    COOLDOWN = 30
    COOLDOWN_SPEED = 0.2
    ENEMY_COLLISION_DMG = 10

    def __init__(self,x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.image = None
        self.rocket = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def get_width(self):
        return self.image.get_width()
    
    def get_height(self):
        return self.image.get_height()

    def move_left(self, speed):
        self.x -= speed
    
    def move_right(self, speed):
        self.x += speed 
    
    def move_down(self, speed):
        self.y += speed
    
    def move_up(self, speed):
            self.y -= speed

    def boundary_right(self, window_width):
        return self.x >= (window_width - self.get_width())

    def boundary_left(self):
        return self.x <= 0
    
    def boundary_down(self, window_height):
        return self.y + self.get_height() >= window_height

    def boundary_up(self):
        return self.y <= 0   

    def shoot(self):
        if self.cool_down_counter == 0:
            laser= LaserBlast(self.x + int(self.rocket.get_width()/2), self.y, self.rocket)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def move_lasers(self, speed, height, object):
        self.cooldown()

        for laser in self.lasers:
            laser.move(speed)

            if laser.off_screen(height):
                self.lasers.remove(laser)

            elif laser.collision(object):
                object.health -= self.ENEMY_COLLISION_DMG
                self.lasers.remove(laser)
            

    
class Player(Ship):
    PLAYER_DMG = 100
    def __init__(self, x, y, image, score= 0, health=100):
        super().__init__(x, y, health)
        self.image = image
        self.score = score
        self.rocket = PLAYER_BULLET
        self.mask = pygame.mask.from_surface(self.image)
        self.max_health = health

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)


    def move_lasers(self, speed, height, objects):
        self.cooldown()
        
        for laser in self.lasers:
            laser.move(speed)

            #if laser goes offscreen remove it
            if laser.off_screen(height):
                self.lasers.remove(laser)

            #if not check if collided with enemies
            else:
                for object in objects:
                    if laser.collision(object):
                        object.health -= self.PLAYER_DMG
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                        if object.health <= 0 and object in objects:
                            object.sound.play()
                            objects.remove(object)
                            self.score += object.points


    def healthbar(self, window):
        pygame.draw.rect(window, COLOR_RED, (self.x, self.y + self.get_height() + 10, self.get_width(), 5))
        pygame.draw.rect(
            window, 
            COLOR_GREEN, 
            (self.x, self.y + self.get_height() + 10, self.get_width() * (self.health/self.max_health), 5))

class Enemy(Ship):
    TYPE_MAP = {
        "soldier" : (ENEMY_UFO, ENEMY_BULLET, UFO_HEALTH, UFO_POINTS),
        "captain" : (ENEMY_UFO_STRONG, ENEMY_BULLET, UFO_STRONGER_HEALTH, UFO_STRONGER_POINTS),
        "boss" : (ENEMY_UFO_BOSS, ENEMY_BULLET, BOSS_HEALTH, UFO_BOSS_POINTS)
    }

    def __init__(self, x, y, type, sound):
        super().__init__(x, y)
        self.image, self.rocket, self.health, self.points = self.TYPE_MAP[type]
        self.sound = sound
        self.mask = pygame.mask.from_surface(self.image)

    def check_off_screen(self, height):
        return (self.y + self.get_height()) >= height


class LaserBlast:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
        

    def move(self, speed):
        self.y += speed
    
    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

    