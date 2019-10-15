import pygame
import sys
import os
import socket
import tkinter as Tkinter
from win32api import GetSystemMetrics
import time

"""   SOCKET   """
with open('info.txt','r') as d:
    data = d.readline()
    port , ip = data.split('>')
    port = int(port.split(':')[1])
    ip = (ip.split(':')[1])
    print(port , ip)

while_value = False
#HOST = '127.0.0.1'
#my_host = '192.168.42.124'
#PORT = 5834

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((ip, port))

BACKGROUND_COLOR = pygame.Color('white')  # The background colod of our window

pygame.init()

"""   LOSE   """
lose = False
times = 0
os.chdir(os.getcwd() + '/spaceship')
"""   EFFECTLER  """
hit = pygame.mixer.Sound('boom9.wav')
hit.set_volume(0.5)
"""    MUSİC    """

pygame.mixer.music.load('Vindication.mp3')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.5)
"""    IMAGES   """

fire = pygame.image.load('fire2.png')
ship_image = pygame.image.load('greenships.png')
ship_image2 = pygame.image.load('othergreenship.png')
bg = pygame.image.load('bg1.png')
laser = pygame.image.load('Red_laser.png')
laser = pygame.transform.scale(laser, (60, 20))

"""---OPTİONS---"""

WIDTH = 1000
HIGHT = 600
font = pygame.font.SysFont("Helvetica", 100)

win = pygame.display.set_mode((WIDTH, HIGHT))
clock = pygame.time.Clock()


def lose_screen():
    label = Tkinter.Label(text='!!!HACKLENDİN!!!', font=('Times', '30'), fg='black', bg='white')
    label.master.overrideredirect(True)
    label.master.geometry(f"+{str(int(GetSystemMetrics(0) / 2))}+{str(int(GetSystemMetrics(1) / 2))}")
    label.master.lift()
    label.master.wm_attributes("-topmost", True)
    label.master.wm_attributes("-disabled", True)
    label.master.wm_attributes("-transparentcolor", "white")
    label.pack()
    label.mainloop()
    print('sleep')
    time.sleep(1)
    print('het')


class other_ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ship_image2
        self.rect = self.image.get_rect()
        self.rect.x = 912
        self.rect.y = 300
        self.fuze_sayisi = 100

    def update(self, *args):
        # pos = str(args[4]).split(':')[0]
        pos = int(args[4])
        fark = pos - self.rect.y
        self.rect.y += fark

    def shoot(self):
        if self.fuze_sayisi == 0:
            pass
        else:
            fuze = Fuze(self.rect.y, 956, '<')
            self.fuze_sayisi -= 1
            all_sprites.add(fuze)
            fuzeler.add(fuze)
            hit.play()


class spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ship_image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 300
        self.kalakn = 100
        self.fuze_sayisi = 100

    def update(self, *args):
        up, down, right, left, pos = args

        if up:
            self.rect.y -= 10
        if down:
            self.rect.y += 10

    def send_Server(self, f):
        if lose:
            print('lose True')
            s.send(('300:3').encode('utf-8'))
        else:
            s.send((str(self.rect.y) + ':' + str(f)).encode('utf-8'))

    def shoot(self):
        if self.fuze_sayisi == 0:
            pass
        else:
            fuze = Fuze(self.rect.y, 200, '>')
            self.fuze_sayisi -= 1
            all_sprites.add(fuze)
            fuzeler.add(fuze)
            hit.play()


class Fuze(pygame.sprite.Sprite):
    def __init__(self, parcay, parcax, yon):
        super().__init__()
        self.image = laser
        # self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = parcax
        self.rect.y = parcay + 40
        self.yon = yon

    def update(self, *args):
        if self.yon == '>':
            self.rect.x += 8
            if self.rect.left > WIDTH:
                self.kill()
        elif self.yon == '<':
            self.rect.x -= 8
            if self.rect.left < 0:
                self.kill()


"""GRUPLAR"""
all_sprites = pygame.sprite.Group()
mermiler = pygame.sprite.Group()
fuzeler = pygame.sprite.Group()

wight_text = font.size('100')[0]
height_text = font.size('100')[1]

ship = spaceship()
all_sprites.add(ship)
ship2 = other_ship()
all_sprites.add(ship2)


def main_loop():
    win.fill((0, 0, 0))
    win.blit(bg, (0, 0))

    fuze_sayisi = font.render(str(ship.fuze_sayisi), 0, (255, 255, 255))
    kalkan = font.render(str(ship.kalakn), 0, (255, 255, 255))

    win.blit(kalkan, (0, 487))
    win.blit(fuze_sayisi, (832, 487))


while True:
    f = 0
    main_loop()
    keys = pygame.key.get_pressed()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ship.shoot()
                f = 1

    ship.send_Server(f)
    up, down, right, left = keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_RIGHT], keys[pygame.K_LEFT]
    poss = s.recv(5).decode('utf-8')

    durum = pygame.sprite.spritecollide(ship, fuzeler, True, collided=pygame.sprite.collide_circle)
    if durum:
        ship.kalakn -= 10
        if ship.kalakn == 0:
            lose = True

    if lose:
        lose_Str = font.render('KAYBETTİN!', 0, (255, 255, 255))
        win.blit(lose_Str, ((WIDTH / 2)-300 , HIGHT / 2))
        if times == 300:
            sys.exit()
        times += 1
        print('time:', times)
        pos = 300
        fuzes = 0
    else:
        pos, fuzes = poss.split(':')

        if int(fuzes) == 1:
            ship2.shoot()
        if int(fuzes) == 3:
            win_str = font.render('KAZANDIN!!!',0,(255,255,255))
            win.blit(win_str ,(((WIDTH / 2)-300 , HIGHT / 2)))
    all_sprites.update(up, down, right, left, pos)
    all_sprites.draw(win)

    pygame.display.update()


