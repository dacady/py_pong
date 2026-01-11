from pygame import *
from random import random

screen = display.set_mode((600, 400))
display.set_caption('Лабиринт')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

bg = GameSprite('bg.png', 0, 0, 600, 400)
p1 = GameSprite('player1.png', 10, 150, 20, 100)
p2 = GameSprite('player2.png', 570, 150, 20, 100)
ball = GameSprite('ball.png', 275, 175, 50, 50)
bx = 3
by = 3
p1w = GameSprite('player1win.png', 0, 0, 600, 400)
p2w = GameSprite('player2win.png', 0, 0, 600, 400)
winner = 0

init()
music = mixer.Sound('music.wav')
hit = mixer.Sound('hit.wav')
win = mixer.Sound('win.wav')
music.play(-1)

font.init()
level_font = font.SysFont('Arial', 70, 1)

level = 1
level_text = level_font.render('level '+str(level), True, (128, 0, 0))

speedup = USEREVENT +1
time.set_timer(speedup, 30000)

fps = time.Clock()
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run=False
        elif e.type == speedup:
            level += 1
            level_text = level_font.render('level '+str(level), True, (128, 0, 0))
            if bx > 0:
                bx += 1
            else:
                bx -= 1
            if by > 0:
                by += 1
            else:
                by -= 1
    if winner == 0:
        keys = key.get_pressed()
        if keys[K_w] and p1.rect.y > 0:
            p1.rect.y -= 10
        if keys[K_s] and p1.rect.y < 300:
            p1.rect.y += 10
        if keys[K_UP] and p2.rect.y > 0:
            p2.rect.y -= 10
        if keys[K_DOWN] and p2.rect.y < 300:
            p2.rect.y += 10
        
        if (ball.rect.y<=0 and by<0) or (ball.rect.y>=350 and by>0):
            by *= -1
        if (sprite.collide_rect(ball, p1) and bx<0) or (sprite.collide_rect(ball, p2) and bx>0):
            bx *= -1
            hit.play()
        if ball.rect.x < 0:
            winner = 2
            win.play()
            music.stop()
        if ball.rect.x > 550:
            winner = 1
            win.play()
            music.stop()
        
        ball.rect.x += bx
        ball.rect.y += by
        
        bg.reset()
        p1.reset()
        p2.reset()
        ball.reset()
        screen.blit(level_text, (10, 10))
    elif winner == 1:
        p1w.reset()
    elif winner == 2:
        p2w.reset()
        
    display.update()
    fps.tick(60)
