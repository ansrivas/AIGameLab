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
        self.myimage = pygame.image.load("bg4.png")
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
        
        pygame.draw.rect(self.image, self.color, (self.x,self.y,self.batdimx, self.batdimy ), self.width)
        self.rot = pygame.transform.rotate(self.image,self.angle )
        
        self.rect = self.rot.get_rect()
        self.rect.center = (253,253)
     
    
    def findPointOnCircle(self,deg):
        
        rad = np.deg2rad(deg)
        y = 253-253 * math.sin(rad)
        x= 253+253 * math.cos(rad)
        print int(x),int(y)
        return int(x),int(y)
    
    def update(self):
        global screen
        self.theta +=self.speed
        self.angle = self.theta - (self.batdimx/213)
        
        self.rot = pygame.transform.rotate(self.image,self.angle)
        print self.rot.get_rect().size
        self.rect = self.rot.get_rect()
        self.rect.center = self.findPointOnCircle(self.theta)
        screen.blit(self.rot,self.rect)
        
        
           
    def display(self):
        global screen
        #pygame.draw.line(screen, self.color, self.start_pos, self.end_pos, 5)
#        pygame.draw.rect(self.rot, self.color, (self.x,self.y,20,20), self.width)
    

all_sprites = pygame.sprite.Group()

    
def main():
    running = True
    backg = Background((width/2,height/2),253,3,blue)
    bat1 = Bat(red,(10,90),(512,253),1)
    bat2 = Bat(blue,(10,50),(0,253),-5)
    all_sprites.add(bat1)
    all_sprites.add(bat2)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
                
                
                
        screen.fill(white)  
        #all_sprites.draw(screen)
        #all_sprites.update()
        
        backg.display()
        bat1.update()
        bat2.update()
        print pygame.mouse.get_pos()
        pygame.display.flip()
        
                
                
if __name__ == "__main__":
    main()   