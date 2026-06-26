from pygame import * 
from random import randint

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.SysFont('Arial', 36)
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN', True, (255, 255 , 255))
lose = font1.render('YOU LOSE!', True, (180 , 0, 0))

img_back = "galaxy.jpg"
img_hero = "rocket.png"
img_enemy = "ufo.png"
score = 0
lost = 0
max_lost = 20
goal = 15

class GameSprite(sprite.Sprite):
    def __init__(self, char_image, char_x, char_y, size_x, size_y, char_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(char_image), (size_x, size_y))
        self.speed= char_speed
        self.rect = self.image.get_rect()
        self.rect.x = char_x
        self.rect.y = char_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))




class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png" , self.rect.centerx , self.rect.top , 15 , 20 , -15)
        bullets.add(bullet)
        



class Enemy(GameSprite):
    def update(self):

        self.rect.y += self.speed

        global lost

        if self.rect.y > win_hight:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1





class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y <0 :
            self.kill()

win_width = 700
win_hight = 500
display.set_caption("Shooter Game") 
window = display.set_mode((win_width, win_hight))
background = transform.scale(image.load(img_back), (win_width, win_hight))

ship = Player("rocket.png", 5, win_hight - 100, 80, 100, 10)
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

finish = False

run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire() 
    
    if not finish:
        window.blit(background,(0,0))

        text_score = font2.render("Score :" + str(score), 1, (85, 39, 67))
        window.blit(text_score, (10, 20))

        text_lose = font2.render("Missed:" +str(lost), 1, (36,  89, 67))
        window.blit(text_lose, (10, 50))


        collides = sprite.groupcollide(monsters,bullets, True,True)
        for c in collides:
            score = score+1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)



        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose , (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))






        ship.update()
        monsters.update()
        ship.reset()
        bullets.update()
        monsters.draw(window)
        bullets.draw(window)

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        for m in monsters:
            m.kill()
        for b in bullets:
            b.kill()
        
        time.delay(3000)
        for i in range(1,6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)
        

    time.delay(50)
