import pygame
import os, sys
from random import choices, randint, choice

if getattr(sys, 'frozen', False):
    game_path = os.path.dirname(sys.executable)
elif __file__:
    game_path = os.path.dirname(__file__)

class Krabby(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        krabby_walk1 = pygame.image.load(game_path + r"\graphics\krabby\krabby_walk1.png")
        krabby_walk1 = pygame.transform.scale(krabby_walk1,(100,110))

        krabby_walk2 = pygame.image.load(game_path + r"\graphics\krabby\krabby_walk2.png")
        krabby_walk2 = pygame.transform.scale(krabby_walk2,(100,110))

        self.krabby = pygame.image.load(game_path + r"\graphics\krabby\krabby.png")
        self.krabby = pygame.transform.scale(self.krabby,(100,100))

        self.frames = [krabby_walk1,krabby_walk2]
        self.frame_index = 0
        self.angle = 0

        self.image = self.krabby
        self.rect = self.image.get_rect(center = (450,250))

        self.speed = 3
        self.collision = False

    def animation(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):            
            self.frame_index = 0
        self.krabby_animation = self.frames[int(self.frame_index)]
        return self.krabby_animation

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]:
            if keys[pygame.K_w]:
                self.angle = 0
                self.image = pygame.transform.rotate(self.animation(),self.angle)
                self.rect.y -= self.speed
                self.animation()
            
            if keys[pygame.K_s]:
                self.angle = 180
                self.image = pygame.transform.rotate(self.animation(),self.angle)
                self.rect.y += self.speed
                self.animation()

            if keys[pygame.K_a]:
                self.angle = 90
                self.image = pygame.transform.rotate(self.animation(),self.angle)
                self.rect.x -= self.speed
                self.animation()

            if keys[pygame.K_d]:
                self.angle = 270
                self.image = pygame.transform.rotate(self.animation(),self.angle)
                self.rect.x += self.speed
                self.animation()
        else: self.image = pygame.transform.rotate(self.krabby,self.angle)

        if keys[pygame.K_SPACE]:
            self.space = True
        else:
            self.space = False

    def collisions(self):
        self.rect.clamp_ip(walkspace)
        self.sprite_collisions = pygame.sprite.spritecollide(krabby_group.sprite,item_group,False)
        
        for sprite in self.sprite_collisions:
            if abs(self.rect.top - sprite.rect.bottom) <= 5:
                self.rect.top = sprite.rect.bottom

            if abs(self.rect.bottom - sprite.rect.top) <= 5:
                self.rect.bottom = sprite.rect.top

            if abs(self.rect.right - sprite.rect.left) <= 5:
                self.rect.right = sprite.rect.left

            if abs(self.rect.left - sprite.rect.right) <= 5:
                self.rect.left = sprite.rect.right

            if self.rect.colliderect(sprite.rect) and not self.space:
                if self.angle == 0:
                    sprite.rect.midbottom = self.rect.midtop
                if self.angle == 180:
                    sprite.rect.midtop = self.rect.midbottom
                if self.angle == 90:
                    sprite.rect.midright = self.rect.midleft
                if self.angle == 270:
                    sprite.rect.midleft = self.rect.midright

        if self.sprite_collisions:
            self.collision = True
        else:
            self.collision = False

    def grab(self):
        if self.collision and self.space:
            if len(self.sprite_collisions) < 2:
                for sprite in item_group:
                    if sprite in self.sprite_collisions:
                        if self.angle == 0:
                            sprite.rect.center = self.rect.midtop
                        if self.angle == 90:
                            sprite.rect.center = self.rect.midleft
                        if self.angle == 180:
                            sprite.rect.center = self.rect.midbottom
                        if self.angle == 270:
                            sprite.rect.center = self.rect.midright

    def update(self):
        self.speed = speed_mod
        self.input()
        self.collisions()
        self.grab()

class Item(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        self.type = type

        self.center_x_pos = [100, 600, 850]
        self.center_x_index = 0
        self.alpha_val = 255
        self.life_time = 130

        if self.type == ["trash"]:
            
            stone = pygame.image.load(game_path + r"\graphics\items\trash\stone.png")
            stone = pygame.transform.scale(stone,(55,45))

            traffic_cone = pygame.image.load(game_path + r"\graphics\items\trash\traffic_cone.png")
            traffic_cone = pygame.transform.scale(traffic_cone,(55,55))

            boohowaer = pygame.image.load(game_path + r"\graphics\items\trash\bo'oh'o'wa'er.png")
            boohowaer = pygame.transform.scale(boohowaer,(96,42))

            item = choice([stone,traffic_cone,boohowaer])

        if self.type == ["fruit"]:
            banana = pygame.image.load(game_path + r"\graphics\items\fruit\banana.png")
            banana = pygame.transform.scale(banana,(50,55))

            coconut = pygame.image.load(game_path + r"\graphics\items\fruit\coconut.png")
            coconut = pygame.transform.scale(coconut,(50,50))

            blueberry = pygame.image.load(game_path + r"\graphics\items\fruit\blueberry.png")
            blueberry = pygame.transform.scale(blueberry,(50,50))

            item = choice([banana,coconut,blueberry])

        if self.type == ["treasure"]:
            diamond = pygame.image.load(game_path + r"\graphics\items\treasure\diamond.png")
            diamond = pygame.transform.scale(diamond,(40,45))

            amulet = pygame.image.load(game_path + r"\graphics\items\treasure\amulet.png")
            amulet = pygame.transform.scale(amulet,(60,60))

            black_rupee = pygame.image.load(game_path + r"\graphics\items\treasure\black_rupee.png")
            black_rupee = pygame.transform.scale(black_rupee,(35,55))

            item = choice([diamond,amulet,black_rupee])

        self.image = item
        self.rect = self.image.get_rect(center = (self.center_x_pos[self.center_x_index],randint(160,160)))

    def item_spawn_update(self):
        sprite_collision = pygame.sprite.spritecollide(self,item_group,False)
        if len(sprite_collision) > 1 and waterspace.contains(self):
            self.center_x_index += 1
            if self.center_x_index >= len(self.center_x_pos):
                self.center_x_index = 2
            self.rect.centerx = self.center_x_pos[self.center_x_index]

    def collisions(self):
        global score,holes
        self.rect.clamp_ip(screen_rect)
        hole_collisions = self.rect.collidelistall(holes)

        if hole_collisions:

            if self.type == ["treasure"]:
                if 0 in hole_collisions:
                    item_group.remove(self)
                    score += 3
                else:
                    item_group.remove(self)
                    score -= 1

            if self.type == ["fruit"]:
                if 1 in hole_collisions:
                    if self.rect.colliderect(hole2_rect):
                        item_group.remove(self)
                        score += 2
                else:
                    item_group.remove(self)
                    score -= 1

            if self.type == ["trash"]:
                if 2 in hole_collisions:
                    if self.rect.colliderect(hole3_rect):
                        item_group.remove(self)
                        score += 1
                else:
                    item_group.remove(self)
                    score -= 1

    def item_despawning(self):
        self.krabby_collision = pygame.sprite.spritecollide(self,krabby_group,False)
        self.image.set_alpha(self.alpha_val)
        self.life_time -= 1
        if waterspace.contains(self.rect) and int(frame_index) == 0 and self.life_time <= 0:
            item_group.remove(self)

        if not waterspace.contains(self.rect) and self.life_time <= 0:
            self.alpha_val -= 2

        if self.alpha_val <= 0 :
            item_group.remove(self)

        if self.krabby_collision:
            self.alpha_val = 255

    def update(self):
        self.item_spawn_update()
        self.item_despawning()
        self.collisions()

def animate_ocean():
    global frame_index,animation_speed,frames

    frame_index += animation_speed
    if frame_index >= len(frames) - 0.1 or frame_index <= 0:
        animation_speed *= -1
    ocean = frames[int(frame_index)]
    screen.blit(ocean,(0,0))

def item_spawning(spawn_cooldown):
    global last_spawn
    now = pygame.time.get_ticks()
    if now - last_spawn >= spawn_cooldown and int(frame_index) == 0:
        last_spawn = now
        item_group.add(Item(choices(["treasure", "fruit", "trash"],cum_weights=[10, 30, 60],k=1)))

def score_render():
    global score

    score_surf = font.render(f"Score: {score}", False, '#3e2016')
    score_rect = score_surf.get_rect(center = (450,30))
    screen.blit(score_surf,score_rect)
    return score

pygame.init()

screen = pygame.display.set_mode((900,500))
screen_rect = screen.get_rect(topleft = (0,0))
pygame.display.set_caption("Krabby Game")
clock = pygame.time.Clock()
font = pygame.font.Font(game_path + r"\font\slkscr.ttf", 50)
score = 0
game_active = False
alpha_val = 255
game_speed = 1500
last_spawn = pygame.time.get_ticks()
spawn_cooldown = 1500
speed_mod = 3

beach_bg = pygame.image.load(game_path + r"\graphics\background\beach.png")

ocean1 = pygame.image.load(game_path + r"\graphics\background\ocean\ocean1.png")
ocean2 = pygame.image.load(game_path + r"\graphics\background\ocean\ocean2.png")
ocean3 = pygame.image.load(game_path + r"\graphics\background\ocean\ocean3.png")
ocean4 = pygame.image.load(game_path + r"\graphics\background\ocean\ocean4.png")

frames = [ocean1,ocean2,ocean3,ocean4]
frame_index = 3
animation_speed = 0.01

game_title = font.render("Krabby Game",False, "#635417")
game_title = pygame.transform.scale(game_title,(600,80))
game_title_rect = game_title.get_rect(center = (450,75))

game_msg = font.render("Press Space to play", False, '#635417')
game_msg_rect = game_msg.get_rect(center = (450,425))

info_table = pygame.image.load(game_path + r"\graphics\background\info_table.png")
info_table = pygame.transform.scale(info_table,(180,200))
info_table_rect = info_table.get_rect(center = (700,250))

info_table2 = pygame.image.load(game_path + r"\graphics\background\info_table2.png")
info_table2 = pygame.transform.scale(info_table2,(180,200))
info_table2_rect = info_table2.get_rect(center = (200,250))

score_board = pygame.image.load(game_path + r"\graphics\background\score_board.png")
score_board_rect = score_board.get_rect(center = (450,30))

krabby_front = pygame.image.load(game_path + r"\graphics\krabby\krabby.png")
krabby_front = pygame.transform.scale(krabby_front,(200,200))
krabby_rect = krabby_front.get_rect(center = (450,250))

treasure_hole = pygame.image.load(game_path + r"\graphics\holes\treasure_hole.png")
treasure_hole = pygame.transform.scale(treasure_hole,(100,100))
treasure_rect = treasure_hole.get_rect(center = (150,450))

fruit_hole = pygame.image.load(game_path + r"\graphics\holes\fruit_hole.png")
fruit_hole = pygame.transform.scale(fruit_hole,(100,100))
fruit_rect = fruit_hole.get_rect(center = (450,450))

trash_hole = pygame.image.load(game_path + r"\graphics\holes\trash_hole.png")
trash_hole = pygame.transform.scale(trash_hole,(100,100))
trash_rect = trash_hole.get_rect(center = (750,450))

hole1_rect = treasure_rect.move(0,50)
hole2_rect = fruit_rect.move(0,50)
hole3_rect = trash_rect.move(0,50)

holes = [hole1_rect,hole2_rect,hole3_rect]

walkspace = pygame.rect.Rect(0,170,900,240)
waterspace = pygame.rect.Rect(0,0,900,200)

krabby_group = pygame.sprite.GroupSingle()
krabby_group.add(Krabby())

item_group = pygame.sprite.Group()

gamespeed_event = pygame.USEREVENT + 1
pygame.time.set_timer(gamespeed_event,20000)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit
            sys.exit()

        if game_active:

            if event.type == gamespeed_event:
                speed_mod += 1
                if speed_mod >= 5:
                    speed_mod = 5
                spawn_cooldown -= 250
                if animation_speed > 0:
                    animation_speed += 0.01
                if animation_speed <= 0:
                    animation_speed -= 0.01
                
                if animation_speed >= 0.07:
                    game_active = False
                if animation_speed <= -0.07:
                    game_active = False
        else:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    score = 0
                    speed_mod = 3

    if game_active:

        screen.blit(beach_bg,(0,0))
        screen.blit(treasure_hole,treasure_rect)
        screen.blit(fruit_hole,fruit_rect)
        screen.blit(trash_hole,trash_rect)

        krabby_group.update()
        krabby_group.draw(screen)

        item_spawning(spawn_cooldown)
        item_group.draw(screen)
        item_group.update()

        animate_ocean()
        screen.blit(score_board,score_board_rect)
        score = score_render()
        
    else:

        screen.fill("#decb8a")
        screen.blit(krabby_front,krabby_rect)
        screen.blit(game_title,game_title_rect)

        game_score = font.render(f"Score: {score}", False, '#635417')
        game_score_rect = game_score.get_rect(center = (450,425))
        if score <= 0:
            screen.blit(game_msg,game_msg_rect)
            screen.blit(info_table,info_table_rect)
            screen.blit(info_table2,info_table2_rect)

        else:
            screen.blit(game_score,game_score_rect)
            animation_speed = 0.01
            item_group.empty()

    pygame.display.update()
    clock.tick(60)