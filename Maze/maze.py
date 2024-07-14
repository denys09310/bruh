from random import choice
from typing import Any
from pygame import *

init()
font.init()
font1 = font.SysFont('Impact', 100)
game_over_text = font1.render('GAME_OVER', True, (255, 0, 0))
win_text = font1.render('YOU WIN', True, (255, 0, 0))
mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
mixer.music.set_volume(0.2)

MAP_WIDTH, MAP_HEIGHT = 25, 20  
TILESIZE = 40  
WIDTH, HEIGHT = MAP_WIDTH * TILESIZE, MAP_HEIGHT * TILESIZE

window = display.set_mode((WIDTH, HEIGHT))
FPS = 60
clock = time.Clock()

bg = image.load('background.jpg')
bg = transform.scale(bg, (WIDTH, HEIGHT))
player2_img = image.load('Lomka 2.png')
player_img = image.load("Lomka.png")
cyborg_img = image.load("cyborg.png")
wall_img = image.load("DesolatedHut.png")
gold_img = image.load("treasure.png")
all_sprites = sprite.Group()

class Sprite(sprite.Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_img, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)

class Player(Sprite):
    def __init__(self, sprite_img, width, height, x, y, controls):
        super().__init__(sprite_img, width, height, x, y)
        self.hp = 100
        self.speed = 2
        self.controls = controls

    def update(self):
        key_pressed = key.get_pressed()
        old_pos = self.rect.x, self.rect.y
        if key_pressed[self.controls['up']] and self.rect.y > 0:
            self.rect.y -= self.speed
        if key_pressed[self.controls['down']] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if key_pressed[self.controls['left']] and self.rect.x > 0:
            self.rect.x -= self.speed
        if key_pressed[self.controls['right']] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        
        collide_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(collide_list) > 0:
            self.rect.x, self.rect.y = old_pos
        enemy_colide = sprite.spritecollide(self, enemys, False, sprite.collide_mask)
        if len(enemy_colide) > 0:
            self.hp -= 100

class Enemy(Sprite):
    def __init__(self, sprite_img, width, height, x, y):
        super().__init__(sprite_img, width, height, x, y)
        self.damage = 100
        self.speed = 2
        self.dir_list = ['right', 'left', "up", "down"]
        self.dir = choice(self.dir_list)

    def update(self):
        old_pos = self.rect.x, self.rect.y
        if self.dir == "right":
            self.rect.x += self.speed
        elif self.dir == "left":
            self.rect.x -= self.speed
        elif self.dir == "up":
            self.rect.y -= self.speed
        elif self.dir == "down":
            self.rect.y += self.speed
        collide_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(collide_list) > 0:
            self.rect.x, self.rect.y = old_pos
            self.dir = choice(self.dir_list)

walls = sprite.Group()
enemys = sprite.Group()


controls1 = {'up': K_w, 'down': K_s, 'left': K_a, 'right': K_d}
controls2 = {'up': K_UP, 'down': K_DOWN, 'left': K_LEFT, 'right': K_RIGHT}

player1 = Player(player_img, TILESIZE - 5, TILESIZE - 5, 300, 300, controls1)
player2 = Player(player2_img, TILESIZE - 5, TILESIZE - 5, 300, 300, controls2)

with open("map.txt", "r") as f:
    map = f.readlines()
    x = 0
    y = 0
    for line in map:
        for symbol in line:
            if symbol == "w":  
                walls.add(Sprite(wall_img, TILESIZE, TILESIZE, x, y))
            if symbol == "p":  
                player1.rect.x = x
                player1.rect.y = y
            if symbol == "o":  
                player2.rect.x = x
                player2.rect.y = y
            if symbol == "g":  
                gold = Sprite(gold_img, 70, 70, x, y)
            if symbol == "e":
                enemys.add(Enemy(cyborg_img, TILESIZE - 5, TILESIZE - 5, x, y))
            x += TILESIZE
        y += TILESIZE
        x = 0

run = True
finish = False
game_win = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    window.blit(bg, (0, 0))

    if player1.hp <= 0 or player2.hp <= 0:
        finish = True
        game_win = False
    
    if sprite.collide_mask(player1, gold) and sprite.collide_mask(player2, gold):
        finish = True
        game_win = True

    all_sprites.draw(window)

    if not finish:
        all_sprites.update()
    else:
        if game_win:
            window.blit(win_text, (300, 300))
        else:
            window.blit(game_over_text, (300, 300))

    display.update()
    clock.tick(FPS)
