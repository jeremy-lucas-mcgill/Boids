import math
class Cell:
    def __init__(self,x,y,speed) -> None:
        self.pos = [x,y]
        self.speed = speed
        self.direction = [0,0]
        self.startHealth = 100
        self.health = 100
        self.color = (255,255,255)
        self.quad = []
    
    def moveDirection(self):
        self.pos = [self.pos[0] + self.direction[0] * self.speed, self.pos[1] - self.direction[1] * self.speed]
    
    def setDirection(self,x,y):
        norm = math.sqrt(x**2 + y**2)
        if (not norm == 0):
            x  = x / norm
            y = y / norm
            self.direction = [x,y]
    
    def setHealth(self,amount):
        self.health += amount
        self.color = (self.health/self.startHealth * 255,self.health/self.startHealth * 255,self.health/self.startHealth * 255)