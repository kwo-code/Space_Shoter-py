from pygame import *
from random import *
from ctypes  import *

mixer.init()
font.init()

bullets               = sprite.Group()
asteroids             = sprite.Group()
lastings_asteroids    = sprite.Group()
bonuses               = sprite.Group()

medium_font           = font.Font(None, 30) 
small_font            = font.Font(None, 20) 

screen_h, screen_w    = windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1)

screen_center = screen_h/2

screen_bonus = screen_w/250

pause_text      = medium_font.render('-pause-', True, (255,202,24))
p_s             = medium_font.render('>>>press space<<<', True, (255,202,24))
background      = transform.scale(image.load('Resurses/images/galaxy.jpg'),(screen_h, screen_w))
display.set_icon(image.load("Resurses/images/ico.bmp"))
screen          = display.set_mode((screen_h, screen_w))
display.set_caption('Spase_Shoter')
clock           = time.Clock()
FPS = 60

game             = True
act              = False
boss_fight       = False
menu             = True
pause            = False

def interface():
    global hp, magasine, hp_text, magasine_text, shot_type, shot_type_interface

    if shot_type == 1:
        shot_type_interface = GameSprite(transform.scale(image.load('Resurses/images/shot_type_1.png'),(30, 30)), screen_h-50, 20, 0)

    if shot_type == 2:
        shot_type_interface = GameSprite(transform.scale(image.load('Resurses/images/shot_type_2.png'),(30, 30)), screen_h-50, 20, 0)

    if hp == 5:
        hp_text = medium_font.render(f'> > > > >', True, (255,202,24))

    if hp == 4:
        hp_text = medium_font.render(f'> > > >', True, (255,202,24))

    if hp == 3:
        hp_text = medium_font.render(f'> > >', True, (255,202,24))
        
    if hp == 2:
        hp_text = medium_font.render(f'> >', True, (255,202,24))

    if hp == 1:
        hp_text = medium_font.render(f'>', True, (255,202,24))

    if magasine >= 5:
        magasine_text = medium_font.render(f'| | | | |', True, (255,202,24))

    if magasine >= 4 and magasine < 5:
        magasine_text = medium_font.render(f'| | | |', True, (255,202,24))

    if magasine >= 3 and magasine < 4:
        magasine_text = medium_font.render(f'| | |', True, (255,202,24))
        
    if magasine >= 2 and magasine < 3:
        magasine_text = medium_font.render(f'| |', True, (255,202,24))

    if magasine >= 1 and magasine < 2:
        magasine_text = medium_font.render(f'| ', True, (255,202,24))

    if magasine >= 0 and magasine < 1:
        magasine_text = medium_font.render(f' ', True, (255,202,24))

def collide():
    global size,bullets,asteroids,score,hp,ship,lastings_asteroids,g_mod,asteroids_
    if sprite.groupcollide(bullets, asteroids, True, True):
        if size >= 50:
            score         += 5
        else:
            score         += 10
        hit = mixer.Sound('Resurses/sounds/hit.mp3')
        hit.set_volume(0.08)
        hit.play()
        asteroids_             -= 1  

    if sprite.groupcollide(bullets, bonuses, True, True):
        mixer.music.load('Resurses/sounds/bonus.mp3')
        mixer.music.set_volume(0.07)
        mixer.music.play()
        score                  += 10
        if hp != 5:
            hp                     += 1

    if sprite.groupcollide(bullets, lastings_asteroids, True, False):
        hit = mixer.Sound('Resurses/sounds/hit_2.mp3')
        hit.set_volume(0.08)
        hit.play() 

    if g_mod == False:
        if sprite.spritecollide(ship, asteroids, True):
            if hp != 1:
                crash = mixer.Sound('Resurses/sounds/crash.ogg')
                crash.set_volume(0.07)
                crash.play()
            g_mod                  = True
            asteroids_             -= 1
            hp                     -= 1
            
        if sprite.spritecollide(ship, lastings_asteroids, False):
            if hp != 1:
                crash = mixer.Sound('Resurses/sounds/crash.ogg')
                crash.set_volume(0.07)
                crash.play()
            g_mod           = True
            asteroids_      -= 1
            hp              -= 1

    if sprite.spritecollide(ship, bonuses, True):
        mixer.music.load('Resurses/sounds/bonus.mp3')
        mixer.music.set_volume(0.07)
        mixer.music.play()
        score                  += 10
        if hp != 5:
            hp                     += 1

def player_processor():
    global immortality_player, g_mod, x_p_pr, g_p_pr, y_p_pr
    if g_mod == True:
        x_p_pr += 1
        if x_p_pr == y_p_pr+5:
            immortality_player    = True
            y_p_pr = x_p_pr
        if x_p_pr == g_p_pr+10:
            immortality_player    = False
            g_p_pr=x_p_pr
        if x_p_pr > 150:
            g_mod                 = False
            immortality_player    = False
    
class GameSprite(sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image    = image
        self.speed    = speed
        self.rect     = self.image.get_rect()
        self.rect.x   = x
        self.rect.y   = y
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        global act, menu,bullets_,magasine,reloading,pause,crush_player,ship,FPS,immortality_player,shot_type
        screen.blit(magasine_text, (self.rect.x-12,self.rect.y+50))

        if menu == True:
            self.rect.x = screen_center-20
        if keys_pressed[K_a] and self.rect.x >= 25 and act == True:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x <= screen_h-47 and act == True:
            self.rect.x += self.speed
        if keys_pressed[K_SPACE] and menu == True:
            act      = True
            menu     = False 
        if immortality_player == True:
            ship = Player(transform.scale(image.load('Resurses/images/rocket_crash.png'),(30, 35)), self.rect.x, self.rect.y, 15)
        if immortality_player != True:
            ship = Player(transform.scale(image.load('Resurses/images/rocket.png'),(30, 35)), self.rect.x, self.rect.y, 15)

    def shot(self):
        global act, menu,bullets_,magasine,reloading,pause,crush_player,ship,FPS,immortality_player,shot_type
        if act == True and magasine != 0 and reloading != True and shot_type == 1:
            bullets_ += 1
            fire = mixer.Sound('Resurses/sounds/fire.ogg')
            fire.set_volume(0.06)
            fire.play()
            magasine -= 1
            bullets.add(Bullet(transform.scale(image.load('Resurses/images/yellow_block.png'),(2, 25)), self.rect.x+14, self.rect.top, 15))
        if act == True and magasine != 1 and reloading != True and shot_type == 2:
            bullets_ += 2
            fire = mixer.Sound('Resurses/sounds/fire.ogg')
            fire.set_volume(0.06)
            fire.play()
            magasine -= 2
            bullets.add(Bullet(transform.scale(image.load('Resurses/images/yellow_block.png'),(2, 25)), self.rect.x+10, self.rect.top, 15))
            bullets.add(Bullet(transform.scale(image.load('Resurses/images/yellow_block.png'),(2, 25)), self.rect.x+18, self.rect.top, 15))
        if reloading == True and act == True:
            non_bullets = mixer.Sound('Resurses/sounds/non_bullets.mp3')
            non_bullets.set_volume(0.06)
            non_bullets.play()
        
class Bullet(GameSprite):
    def update(self):
        global bullets_, massage_type
        if act == True:
            self.rect.y -= self.speed
        if self.rect.y < 0:
            bullets_ -= 1
            miss = mixer.Sound('Resurses/sounds/miss.mp3')
            miss.set_volume(0.07)
            miss.play()
            self.kill()
        if menu == True:
            self.kill()
        
class Asteroid(GameSprite):
    def update(self):
        global screen_w,asteroids_,act,score,bullets_
        if act == True:
            self.rect.y += self.speed
        if self.rect.y > screen_w:
            asteroids_ -= 1
            self.kill()     
        if menu == True:
            self.kill()

class General(GameSprite):
    def update(self):
        global screen_w,asteroids_,act,score,bullets_
        if act == True:
            self.rect.y += self.speed
        if self.rect.y > screen_w:
            self.kill()     
        if menu == True:
            self.kill()

ship = Player(transform.scale(image.load('Resurses/images/rocket.png'),(30, 35)), screen_center-20, screen_w-100, 15)

shot_type_interface = GameSprite(transform.scale(image.load('Resurses/images/shot_type_1.png'),(30, 30)), screen_h-50, 20, 0)

while game:
    keys_pressed = key.get_pressed()

    screen.blit(background,(0, 0))
    for e in event.get():
        if e.type == QUIT:
            game  = False  
        if e.type == KEYDOWN and e.key == K_ESCAPE:
            game  = False 
        if e.type == KEYDOWN and e.key == K_w:
            ship.shot()
        if e.type == KEYDOWN and e.key == K_SPACE:
            if act == True and pause == False and menu == False:
                pause,act        = True,False
            else:
                pause,act        = False,True
        if e.type == KEYDOWN and e.key == K_s:
            if time_dilation == False:
                time_dilation = True
            else:
                time_dilation = False

    if act == True:

        player_processor()
        interface()

        FPS = 60
        time_ += 1

        if time_dilation_ != 200:
            time_dilation_ += 1
        
        if keys_pressed[K_1]:
            shot_type = 1

        if keys_pressed[K_2]:
            shot_type = 2

        if g_mod == False:
            x_p_pr = 0
            y_p_pr = 0
            g_p_pr = 0

        if asteroids_ < spavn_asteroids + screen_bonus:
            random_type = randint(1, 100)
            if random_type < 10 and score > 100:
                size = randint(60, 100)
                lastings_asteroids.add(General(transform.scale(image.load('Resurses/images/asteroid_2.png'),(size, size)), randint(20, screen_h-100), 2, randint(3, 4) + sprite_speed_boost))
            if random_type > 10 and random_type  < 12:
                bonuses.add(General(transform.scale(image.load('Resurses/images/bonus.png'),(50, 50)), randint(20, screen_h-100), 2, randint(4, 5) + sprite_speed_boost))
            else:
                asteroids_ += 1
                size = randint(30, 100)
                asteroids.add(Asteroid(transform.scale(image.load('Resurses/images/Asteroid.png'),(size, size)), randint(20, screen_h-100), 2, randint(3, 5) + sprite_speed_boost))

        if score >= old_score+100:
            mixer.music.load('Resurses/sounds/extra_life.mp3')
            mixer.music.set_volume(0.07)
            mixer.music.play()
            old_score = score
            sprite_speed_boost += 0.1
            spavn_asteroids += 1
            if hp < 5:
                hp += 1

        if hp == 0:
            fire = mixer.Sound('Resurses/sounds/fail.mp3')
            fire.set_volume(0.20)
            fire.play()
            menu            = True
            act             = False
            boss_fight      = False

        if magasine <= 0.9 and shot_type == 1:
            reloading = True

        if magasine <= 1.9 and shot_type == 2:
            reloading = True

        if magasine >= 5:
            reloading = False

        if reloading == True:
            magasine += 0.03

        if score > data:
            with open('Resurses/statistics.txt', 'w') as file:
                file.write(d_score)

        if time_dilation == True and time_dilation_ > 5:
            FPS = 30
            time_dilation_ -= 3

        if time_dilation_ < 5:
            time_dilation = False

    if menu == True:
        reloading, crash_player          = False, False
        immortality_player, g_mod        = False, False
        pause, time_dilation             = False, False
        time_dilation_                   = 1
        shot_type,m_s_t_x                = 1, 130
        magasine, bullets_               = 5, 0
        sprite_speed_boost, hp           = 0, 5
        spavn_asteroids, asteroids_      = 5, 0
        score, old_score                 = 0, 0
        time_, old_time_                 = 0, 0
        hp_text                          = medium_font.render(f'> > > > >', True, (255,202,24))  
        magasine_text                    = medium_font.render(f'| | | | |', True, (255,202,24))  
        screen.blit(p_s, (screen_center-100,screen_w-150))

    time_dilation_indicator = GameSprite(transform.scale(image.load('Resurses/images/yellow_block.png'),(time_dilation_, 3)), screen_center-(time_dilation_/2)-10, screen_w-10, 0)

    with open('Resurses/statistics.txt', 'r') as file:
        data = file.read()
        data = int(data)

    d_score = str(score)   

    if score >= 1000:
            m_s_t_x = 140
    if score >= 10000:
            m_s_t_x = 150

    bullets.draw(screen)
    bullets.update()
    asteroids.draw(screen)
    asteroids.update()
    lastings_asteroids.draw(screen)
    lastings_asteroids.update()
    bonuses.draw(screen)
    bonuses.update()
    shot_type_interface.reset()
    ship.reset()
    ship.update()
    time_dilation_indicator.reset()

    collide()

    max_score_text = small_font.render(f'max score: {data}', True, (255,202,24))
    score_text = medium_font.render(f'score: {score}', True, (255,202,24))
    screen.blit(score_text,       (20,20))
    screen.blit(hp_text,          (20,40))
    screen.blit(max_score_text,   (m_s_t_x,20))

    if pause == True:
        screen.blit(pause_text, (screen_center-45, screen_center))

    display.update()
    clock.tick(FPS)