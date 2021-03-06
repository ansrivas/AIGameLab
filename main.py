'''
Created on Feb 19, 2015

@author: Ankur
'''
import pygame, math,random
import numpy as np
from sympy.mpmath import unitvector

class Color():
    white=(255,255,255)
    blue = (0,255,255)
    red = (255,0,0)
    snow = (205,201,201)
    palegreen= (152,251,152)

    def __init__(self):
        pass

    def randomcolor(self):
        randcolor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        return randcolor
    
    
width,height = (700,530)
screen =  pygame.display.set_mode((width, height))
debug = False


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./resource/ball.gif")
        self.rect = self.image.get_rect()  
        #this is the first position from where the ball would be loaded, 
        #need to randomize it   
        self.rect.centerx,self.rect.centery = (100,100)
        self.speedx = 0.5
        self.speedy = 2
        self.angle = math.pi/2
        
     
    def update(self):
        global screen
        #check if adding this speed makes the coordinates go beyond the limits of circle
        radius = 250
        dist = math.hypot(self.rect.x+self.speedx - 266 ,self.rect.y+self.speedy -266)
        
        if(dist < radius):
            
            self.rect.x +=self.speedx
            self.rect.y +=self.speedy
        else:
            #fix the position here

            print "reaching outside------------>"
        screen.blit(self.image, self.rect)
        self.collisionwithcircle()
    

    def collisionwithcircle(self):
        #this the direction vector of the ball
        dx,dy = (self.rect.centerx -266,self.rect.centery-266)        
        #dx and dy are the direction vectors from center of circle
         
        dist = (dx**2 +dy**2)**0.5 
        maxdist = 250 - self.rect.size[0]/2 +1
        
        #print dist, maxdist, self.rect.center
        # self.speedx , self.speedy are the velocity vectors
        if(dist > maxdist): 
            print "collision occurred"
            magofdirection = math.hypot(dx, dy)
            if(magofdirection == 0):
                magofdirection = 1
            unitvectorx = float(dx/magofdirection)
            unitvectory = float(dy/magofdirection)
            dotproduct = self.speedx*unitvectorx + self.speedy*unitvectory
            self.speedx = -2*dotproduct*unitvectorx + self.speedx
            self.speedy = -2*dotproduct*unitvectory + self.speedy
            print self.speedx, self.speedy

            
    def display(self):
        global screen
        
        #pygame.draw.circle(screen, self.color, (self.x,self.y), self.size, self.width)
 

class Background():
    def __init__(self,(x,y),size,width,color):
        self.colorobj = Color()
        
        self.size = size
        self.width = width
        self.color = color
        self.myimage = pygame.image.load("./resource/bg4.png")
        self.imagerect = self.myimage.get_rect()
        self.imagerect.x,self.imagerect.y = ( 10, 10)
        self.x,self.y = self.imagerect.center
         
        
    def update(self):
        global screen
        screen.blit(self.myimage, self.imagerect)
        #use it to produce game-over effects for few seconds
        #self.color = self.colorobj.randomcolor()
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.size, self.width)


class Bat(pygame.sprite.Sprite):
    def __init__(self,color,batdimension,startpos,speed):
        pygame.sprite.Sprite.__init__(self)
      
        self.color = color
        self.width = width
        self.image = pygame.Surface(batdimension)
        self.image.fill(Color.white)
        self.image.set_colorkey(Color.white)
        
        self.x= 0
        self.y =0
        self.angle = 1
        self.theta =  0 
        self.speed = speed
        self.batdimx, self.batdimy = batdimension
        
        self.image = pygame.image.load("./resource/bat_100_20.png")
        if(debug):
            pygame.draw.rect(self.image, self.color, (self.x,self.y,self.batdimx, self.batdimy ), self.width)
        self.rot = pygame.transform.rotate(self.image,self.angle )
        
        self.rect = self.rot.get_rect()
        self.rect.center = (266,266)
     
    
    def findPointOnCircle(self,deg):
        """
        Give an angle in degrees and we will get a corresponding point on circle w.r.t to this angle in clockwise.
        """
        rad = np.deg2rad(deg)
        y = 266 - 250 * math.sin(rad)
        x = 266 + 250 * math.cos(rad)
        return int(x),int(y)
    
    def update(self):
        global screen
        #self.theta += self.speed
        if(self.theta > 360):
            self.theta = 0
        self.angle  = float(self.theta) - float(self.batdimx/213)
        
        self.rot = pygame.transform.rotate(self.image,self.angle)
        self.rect = self.rot.get_rect()
        self.rect.center = self.findPointOnCircle(self.theta)
        screen.blit(self.rot,self.rect)
    
    def moveBat(self,js_hor,js_vert):
        #here took -0.1 since the buffer is not being cleared properly, values is being set to -0.000003
        if(js_vert < -0.1):
            self.theta += self.speed 
        if(js_vert >0.0 ):
            self.theta -=self.speed
            
           
    def display(self):
        global screen
        #pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, 5)
#        pygame.draw.rect(self.rot, self.color, (self.x,self.y,20,20), self.width)
    

all_sprites = pygame.sprite.Group()


class GameState:
    RUNNING, PAUSED, RESETTED, STOPPED = range(0, 4) 

class CMain():
    def __init__(self):
        self.bat1 = None
        self.bat2 = None
        self.gamestate = None
        self.color = Color()
        pygame.init()
        pygame.joystick.init()
        self.joystickCount = pygame.joystick.get_count()
        for i in range(self.joystickCount):
            #We need to initialize the individual joystick instances to receive the events
            pygame.joystick.Joystick(i).init()
        
        
    def main(self):
        
        self.gamestate = GameState.STOPPED
        
        running = True
        backg = Background((width/2,height/2),253,5,Color.palegreen)
        bat1 = Bat(Color.red,(10,90),(512,253),10)
        bat2 = Bat(Color.blue,(10,50),(0,253),-5)
        ball = Ball()
        all_sprites.add(bat1)
        all_sprites.add(bat2)
        all_sprites.add(ball)
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.JOYBUTTONDOWN:
                    if(self.gamestate == GameState.STOPPED):
                        self.gamestate = GameState.RUNNING
                        #when the player presses start button then the joystick gets activated
                        #game state will change here to started.
                        self.bat1 = pygame.joystick.Joystick(event.joy)
                    
                if event.type == pygame.JOYAXISMOTION:
                    if(self.gamestate == GameState.RUNNING):
                        jy_bat1_horizontal =  (self.bat1.get_axis(0))
                        jy_bat1_vertical =  (self.bat1.get_axis(1))
                        #print jy_bat1_horizontal,jy_bat1_vertical
                       
                        bat1.moveBat(jy_bat1_horizontal, jy_bat1_vertical)
                        #just clearing the variables
                        jy_bat1_horizontal = 0
                        jy_bat1_vertical  = 0
                        '''
                        if(jy_bat1_horizontal < 0 ):
                            
                            print "horizontal negative"
                        elif(jy_bat1_horizontal > 0 ):
                            print "horizontal positive"
                        elif( jy_bat1_vertical <0 ):
                            print "vertical positive"
                        elif(jy_bat1_vertical >0 ):
                            print "vertical negative"   
                        '''
            screen.fill(Color.white)
            backg.update()  
            all_sprites.update()
            pygame.display.flip()
            clock.tick(60)
            
        pygame.quit()           
                
if __name__ == "__main__":
    obj = CMain()
    obj.main() 