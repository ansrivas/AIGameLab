'''
Created on Feb 19, 2015

@author: Ankur
'''
import pygame, math
import numpy as np

white=(255,255,255)
blue = (0,255,255)
red = (255,0,0)
width,height = (513,513)
screen =  pygame.display.set_mode((width, height))
debug = False

class Ball():
    def __init__(self,(x,y),size,width,color):
        
        self.x,self.y = x,y
        self.size = size
        self.width = width
        self.color = color
        
    def display(self):
        global screen
        
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.size, self.width)
 

class Background():
    def __init__(self,(x,y),size,width,color):
        
        self.x,self.y = x,y
        self.size = size
        self.width = width
        self.color = color
        self.myimage = pygame.image.load("./resource/bg4.png")
        self.imagerect = self.myimage.get_rect()
        
    def display(self):
        global screen
        screen.blit(self.myimage, self.imagerect)
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.size, self.width)

class Bat(pygame.sprite.Sprite):
    def __init__(self,color,batdimension,startpos,speed):
        pygame.sprite.Sprite.__init__(self)
      
        self.color = color
        self.width = width
        self.image = pygame.Surface(batdimension)
        self.image.fill(white)
        self.image.set_colorkey(white)
        
        self.x= 0
        self.y =0
        self.angle = 0
        self.theta =  0 
        self.speed = speed
        self.batdimx, self.batdimy = batdimension
        
        self.image = pygame.image.load("./resource/bat_100_20.png")
        if(debug):
            pygame.draw.rect(self.image, self.color, (self.x,self.y,self.batdimx, self.batdimy ), self.width)
        self.rot = pygame.transform.rotate(self.image,self.angle )
        
        self.rect = self.rot.get_rect()
        self.rect.center = (253,253)
     
    
    def findPointOnCircle(self,deg):
        
        rad = np.deg2rad(deg)
        y = 253- 253 * math.sin(rad)
        x = 253+ 253 * math.cos(rad)
        return int(x),int(y)
    
    def update(self):
        global screen
        self.theta += self.speed
        self.angle  = self.theta - (self.batdimx/213)
        
        self.rot = pygame.transform.rotate(self.image,self.angle)
        self.rect = self.rot.get_rect()
        self.rect.center = self.findPointOnCircle(self.theta)
        screen.blit(self.rot,self.rect)
        
        
           
    def display(self):
        global screen
        #pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, 5)
#        pygame.draw.rect(self.rot, self.color, (self.x,self.y,20,20), self.width)
    

all_sprites = pygame.sprite.Group()


class CMain():
    def __init__(self):
        self.bat1 = None
        self.bat2 = None
        pygame.init()
        pygame.joystick.init()
        self.joystickCount = pygame.joystick.get_count()
        for i in range(self.joystickCount):
            #We need to initialize the individual joystick instances to receive the events
            pygame.joystick.Joystick(i).init()
        
        
    def main(self):
        running = True
        backg = Background((width/2,height/2),253,3,blue)
        bat1 = Bat(red,(10,90),(512,253),0.5)
        bat2 = Bat(blue,(10,50),(0,253),-2)
        all_sprites.add(bat1)
        all_sprites.add(bat2)
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.JOYBUTTONDOWN:
                    #Set the joystick instance of PacMan
                    self.bat1 = pygame.joystick.Joystick(event.joy)
                    
                if event.type == pygame.JOYAXISMOTION:
                    jy_bat1_horizontal = self.bat1.get_axis(0)
                    jy_bat1_vertical = self.bat1.get_axis(1)
                    
                   
                    if(jy_bat1_horizontal < 0):
                        print "horizontal negative"
                    elif(jy_bat1_horizontal > 0):
                        print "horizontal positive"
                    if(jy_bat1_vertical > 0):
                        print "vertical positive"
                    elif(jy_bat1_vertical < 0): 
                        print "vertical negative"   
                
            screen.fill(white)  
            backg.display()
            all_sprites.update()
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()           
                
if __name__ == "__main__":
    obj = CMain()
    obj.main() 