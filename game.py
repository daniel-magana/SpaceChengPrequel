import pygame, sys, math, random
from pygame.locals import *

pygame.init()

FPS = 30 
fpsClock = pygame.time.Clock()

#tamaño de ventana
width=800
height=600

# set up the window
screen = pygame.display.set_mode((width,height), 0, 32)
scr_rec=screen.get_rect()
pygame.display.set_caption('Space Cheng: The Prequel')

#colores
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
GREEN = ( 57, 255,  20)
RED   = (255,   0,   0)

def dist(x1,y1,x2,y2):  
    return math.sqrt((x2-x1)**2 + (y2-y1)**2) 

def text_objects(font, text, color, text_center):
    rendered = font.render(text, True, color)
    return rendered, rendered.get_rect(center=text_center)

def DrawBar(pos, size, borderC, barC, progress):
    #pygame.draw.rect(screen, borderC, (*pos, *size), 1)
    pygame.draw.rect(screen, borderC, ([pos[0],pos[1]], [size[0],size[1]]), 1)
    innerPos  = (pos[0]+3, pos[1]+3)
    innerSize = ((size[0]-6) * progress, size[1]-6)
    #pygame.draw.rect(screen, barC, (*innerPos, *innerSize))
    pygame.draw.rect(screen, barC, ([innerPos[0],innerPos[1]], [innerSize[0],innerSize[1]]))

class Nave:
    radio=10
    vida=3
    x = width/2
    y = height/3
    speed=5
    rotspeed=5
    widthNave=30
    heightNave=30

    def __init__(self):
        self.image = pygame.image.load('nave.png')
        self.original_image=pygame.image.load('nave.png')
        self.angle=0
        self.rect = self.image.get_rect().move((self.x,self.y))
        self.radio=10

    def getvida(self):
        return self.vida

    def getspeed(self):
        return self.speed

    def setspeed(self,s):
        self.speed=s

    def daño(self,d):
        self.vida-=d

    def imag(self):
        return self.image

    def getradio(self):
        return self.radio

    def rec(self):
        return self.rect

    def ang(self):
        return self.angle
    
    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def advance(self):
        if self.y<=(height-self.heightNave) and self.y>=0:
            self.y -= self.speed*math.cos(self.angle*math.pi/180)
        elif self.y>(height-self.heightNave):
            self.y=(height-self.heightNave)
        elif self.y<0:
            self.y=0
        self.rect.top=self.y

        if self.x<=(width-self.widthNave) and self.x>=0:
            self.x -= self.speed*math.sin(self.angle*math.pi/180)
        elif self.x>(width-self.widthNave):
            self.x=(width-self.widthNave)
        elif self.x<0:
            self.x=0
        self.rect.left=self.x

    def back(self):
        if self.y<height and self.y>0:
            self.y += self.speed*math.cos(self.angle*math.pi/180)
            self.rect.top=self.y
        elif self.y>height:
            self.y=height
        elif self.y<0:
            self.y=0
        self.rect.top=self.y

        if self.x<width and self.x>0:
            self.x += self.speed*math.sin(self.angle*math.pi/180)
            self.rect.left=self.x
        elif self.x>width:
            self.x=width
        elif self.x<0:
            self.x=0
        self.rect.left=self.x
    
    def rotleft(self):
        self.angle += self.rotspeed % 360  # Value will reapeat after 359. This prevents angle to overflow.
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        x, y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (x, y)  # Put the new rect's center at old center.

    def rotright(self):
        self.angle -= self.rotspeed % 360  # Value will reapeat after 359. This prevents angle to overflow.
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        x, y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (x, y)  # Put the new rect's center at old center.

class Bala:
    x=0
    y=0
    speed=8

    def __init__(self,x,y,ang,hostil=False):
        self.hostil=hostil
        self.x=x
        self.y=y
        self.angle=ang
        if(not hostil):
            self.image=pygame.image.load('bala.png')
            self.original_image=pygame.image.load('bala.png')
        else:
            self.image=pygame.image.load('bala_enemiga.png')
            self.original_image=pygame.image.load('bala_enemiga.png')
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect().move((self.x,self.y))

    def move(self):
        self.x -= self.speed*math.sin(self.angle*math.pi/180)
        self.y -= self.speed*math.cos(self.angle*math.pi/180)
        self.rect.center=(self.x,self.y)

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def imag(self):
        return self.image
    
    def rec(self):
        return self.rect
    
    def ang(self):
        return self.angle

    def bad(self):
        return self.hostil

class Meteoro(Nave,Bala):
    def __init__(self):
        self.spawn()                 

        self.vida=2
        self.speed=3
        self.rotspeed=random.randint(-3,3)
        self.radio=25
        self.image = pygame.image.load('meteor.png')
        self.original_image=pygame.image.load('meteor.png')
        self.image_angle=random.randint(0,359)
        self.image = pygame.transform.rotate(self.original_image, self.image_angle)
        self.rect = self.image.get_rect().move((self.x,self.y))

    def spawn(self):
        #ubicacion de partida y a que punto va
        if(random.randint(0,1)):
            self.x=random.randint(0,width)
            self.y=random.choice([0,height])
            if(self.y==height):
                self.angle=random.randint(-45,45)
            else:
                self.y-=80
                self.angle=random.randint(135,225)
        else:
            self.x=random.choice([0,width])
            self.y=random.randint(0,height)
            if(self.x==width):
                self.angle=random.randint(45,135)
            else:
                self.x-=80
                self.angle=random.randint(225,315)  

    def move(self):
        super(Meteoro,self).move()
        self.image_angle += self.rotspeed % 360  # Value will reapeat after 359. This prevents angle to overflow.
        self.image = pygame.transform.rotate(self.original_image, self.image_angle)
        x, y = self.rect.center  # Save its current center.
        self.rect = self.image.get_rect()  # Replace old rect with new rect.
        self.rect.center = (x, y)  # Put the new rect's center at old center.

class Meteoro_2nd(Meteoro):
    def __init__(self,orix,oriy,angulo,n):
        self.x=orix
        self.y=oriy
        self.vida=1
        self.speed=4
        self.radio=10
        self.angle=angulo+n*30
        self.image = pygame.image.load('meteor2.png')
        self.original_image=pygame.image.load('meteor2.png')
        self.image_angle=random.randint(0,359)
        self.image = pygame.transform.rotate(self.original_image, self.image_angle)
        self.rect = self.image.get_rect().move((self.x,self.y))

class Red_star(Meteoro):
    def __init__(self):
        self.spawn()                 

        self.vida=3
        self.speed=2
        self.rotspeed=random.randint(-3,3)
        self.radio=25
        self.image = pygame.image.load('star.png')
        self.original_image=pygame.image.load('star.png')
        self.image_angle=random.randint(0,359)
        self.image = pygame.transform.rotate(self.original_image, self.image_angle)
        self.rect = self.image.get_rect().move((self.x,self.y))

    def explode(self,cantidad):
        balas=[]
        for i in range(cantidad):
            bala=Bala(self.x,self.y,self.angle+i*360/cantidad,True)
            balas.append(bala)
        return balas

def game_loop():
    shoot_sound = pygame.mixer.Sound('shoot.wav')
    lvl_sound = pygame.mixer.Sound('lvl.wav')
    exp1_sound = pygame.mixer.Sound('exp1.wav')
    exp2_sound = pygame.mixer.Sound('exp2.wav')
    damage_sound = pygame.mixer.Sound('damage.wav')
    
    pygame.mixer.music.load('Main_song.mp3')
    pygame.mixer.music.play(-1)

    nave=Nave()
    nave.setspeed(5)
    
    #nivel
    level=1

    puntaje=0
    meta=100

    nivel_terminado=False

    #listas de objetos
    balas=[]
    meteoros=[]

    #temporizadores
    temporizador_bala=1000
    delay_bala=250
    t_meteoro=2000
    d_meteoro=1000
    t_daño=750
    d_daño=750
    t_cambio_nivel=4000
    d_cambio_nivel=4000

    t_barra=4000
    descontando=False

    The_game=True

    while The_game:

        screen.fill(BLACK)

        #temporizadores
        temporizador_bala+=FPS
        t_meteoro+=FPS
        t_daño+=FPS
        if(t_cambio_nivel<=d_cambio_nivel):
            t_cambio_nivel+=FPS

        keys = pygame.key.get_pressed()

        #controles
        if(nave.getvida()>0):
            #disparo
            if keys[pygame.K_SPACE] and temporizador_bala>delay_bala:
                shoot_sound.play()
                b=Bala(nave.rec().center[0]-15*math.sin(nave.ang()*math.pi/180),nave.rec().center[1]-15*math.cos(nave.ang()*math.pi/180),nave.ang())
                balas.append(b)
                temporizador_bala=0

            #movimiento
            if keys[pygame.K_LEFT]:
                nave.rotleft()
            elif keys[pygame.K_RIGHT]:
                nave.rotright()
            elif keys[pygame.K_UP]:
                nave.advance()
            elif keys[pygame.K_DOWN]:
                nave.back()
        else:
            if keys[pygame.K_SPACE] and t_cambio_nivel>=d_cambio_nivel/4:
                return
        
        #generar meteoros
        if(t_meteoro>d_meteoro):
            if(level>4 and random.randint(0,3)==0):
                e=Red_star()
                meteoros.append(e)
            m=Meteoro()
            m.setspeed(3+0.1*level)
            meteoros.append(m)
            t_meteoro=0

        #Display nave
        if(nave.getvida()>0):
            screen.blit(nave.imag(), nave.rec())

        #Display balas, daño a meteoros y nave
        try:
            for bal in balas:
                bal.move()
                if bal.bad():
                    if dist(bal.rec().center[0],bal.rec().center[1],nave.rec().center[0],nave.rec().center[1])<nave.getradio():
                        if not nivel_terminado:
                            damage_sound.play()
                            nave.daño(1)
                            if nave.getvida()<1:
                                t_cambio_nivel=0
                        t_daño=0
                else:
                    for met in meteoros:
                        if(dist(bal.rec().center[0],bal.rec().center[1],met.rec().center[0],met.rec().center[1])<met.getradio()):
                            balas.remove(bal)
                            met.daño(1)
                            if(met.getvida()<1 and puntaje<meta and t_cambio_nivel>=d_cambio_nivel):
                                if(isinstance(met,Meteoro_2nd)):
                                    exp2_sound.play()
                                    puntaje+=30
                                elif(isinstance(met,Red_star)):
                                    exp1_sound.play()
                                    ex=met.explode(level)
                                    for e in ex:
                                        balas.append(e)
                                    puntaje+=150
                                else:
                                    exp1_sound.play()
                                    puntaje+=50
                                if(puntaje>=meta):
                                    puntaje=meta
                                    nivel_terminado=True
                                    lvl_sound.play()
                if(bal.getx()<0 or bal.getx()>width or bal.gety()<0 or bal.gety()>height):
                    balas.remove(bal)
                    del bal
                else:
                    screen.blit(bal.imag(), bal.rec())
        except ValueError:
            print("Value error en balas")
            for bal in balas:
                bal.move()
                screen.blit(bal.imag(), bal.rec())

        #Display meteoros, daño a nave
        for met in meteoros:
            met.move()
            if(t_daño>d_daño and dist(nave.rec().center[0],nave.rec().center[1],met.rec().center[0],met.rec().center[1])<met.getradio()+nave.getradio()):
                if not nivel_terminado:
                    damage_sound.play()
                    nave.daño(1)
                    if nave.getvida()<1:
                        t_cambio_nivel=0
                t_daño=0
            if(met.getx()<-100 or met.getx()>width+100 or met.gety()<-100 or met.gety()>height+100 or met.getvida()<1):
                if(level>2 and met.getvida()<1 and not isinstance(met,Meteoro_2nd) and not isinstance(met,Red_star)):
                    m1=Meteoro_2nd(met.rec().center[0],met.rec().center[1],met.ang(),1)
                    m2=Meteoro_2nd(met.rec().center[0],met.rec().center[1],met.ang(),-1)
                    m1.setspeed(4+0.15*level)
                    m2.setspeed(4+0.15*level)
                    meteoros.append(m1)
                    meteoros.append(m2)
                meteoros.remove(met)
                del met
            else:
                screen.blit(met.imag(), met.rec())

        #cambio de nivel
        if(nivel_terminado):
            nivel_terminado=False
            level+=1
            t_meteoro=-4000
            t_daño=-4000
            delay_bala-=10
            d_meteoro-=40
            d_daño-=10
            nave.setspeed(nave.getspeed()+0.2)
            if(level%3==0):
                nave.daño(-1)
            meta+=100
            puntaje=0
            t_cambio_nivel=0
            descontando=True

        #quit game
        for event in pygame.event.get(): # event handling loop
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

        #HUD
        fuente=pygame.font.Font("8-BIT_WONDER.TTF",20)
        text="Level"
        screen.blit(text_objects(fuente, text, WHITE, [100,scr_rec.top+20])[0],text_objects(fuente, text, WHITE, [100,scr_rec.top+20])[1])
        fuente=pygame.font.Font("8-BIT_WONDER.TTF",20)
        text=str(level)
        screen.blit(*text_objects(fuente, text, WHITE, [180,scr_rec.top+20]))
        
        if(nave.getvida()>0):
            fuente=pygame.font.Font("8-BIT_WONDER.TTF",20)
            text="Life"
            screen.blit(*text_objects(fuente, text, WHITE, [scr_rec.right-150,scr_rec.top+20]))
            fuente=pygame.font.Font("8-BIT_WONDER.TTF",20)
            text=str(nave.getvida())
            screen.blit(*text_objects(fuente, text, GREEN, [scr_rec.right-75,scr_rec.top+20]))

            if(not descontando):
                DrawBar([50,height-50],[width-100,30],WHITE,WHITE,puntaje/meta)
            elif(descontando):
                t_barra-=FPS
                DrawBar([50,height-50],[width-100,30],WHITE,WHITE,t_barra/d_cambio_nivel)
                if(t_barra<=0):
                    descontando=False
                    t_barra=d_cambio_nivel
        else:
            fuente=pygame.font.Font("8-BIT_WONDER.TTF",50)
            text="GAME OVER"
            screen.blit(*text_objects(fuente, text, RED, [scr_rec.center[0],scr_rec.center[1]-100]))
            if t_cambio_nivel>=d_cambio_nivel/4:
                fuente=pygame.font.Font("8-BIT_WONDER.TTF",15)
                text="[press SPACE to play again]"
                screen.blit(*text_objects(fuente, text, WHITE, [scr_rec.center[0],scr_rec.bottom-25]))
        
        pygame.display.update()
        fpsClock.tick(FPS)

def intro():

    in_intro=True

    pygame.mixer.music.load('Intro_song.mp3')
    pygame.mixer.music.play(-1)

    while in_intro:
        #quit game
        for event in pygame.event.get(): # event handling loop
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key==pygame.K_SPACE:
                        in_intro=False

        screen.fill(BLACK)
        fuente=pygame.font.Font("8-BIT_WONDER.TTF",50)
        text="Space CHENG"
        screen.blit(*text_objects(fuente, text, WHITE, [scr_rec.center[0],scr_rec.center[1]-100]))
        fuente=pygame.font.Font("8-BIT_WONDER.TTF",35)
        text="The PreQuel"
        screen.blit(*text_objects(fuente, text, WHITE, [scr_rec.center[0],scr_rec.center[1]]))
        fuente=pygame.font.Font("8-BIT_WONDER.TTF",20)
        text="[press SPACE to play]"
        screen.blit(*text_objects(fuente, text, WHITE, [scr_rec.center[0],scr_rec.bottom-25]))
        fuente=pygame.font.Font("8-BIT_WONDER.TTF",15)
        text="Xhi"
        screen.blit(*text_objects(fuente, text, WHITE, [width-20,height-10]))

        pygame.display.update()
        fpsClock.tick(FPS)

intro()
while True:
    game_loop()