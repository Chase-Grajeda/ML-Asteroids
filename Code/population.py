import pygame 
import math 
import numpy as np 
from ship import * 
from roid import * 
from bullet import * 
from vision import * 
from network import * 

class Population(): 
    def __init__(self): 
        
        super().__init__() 
        # Fitness 
        self.gameOver = False 
        self.timeAlive = 0 
        self.score = 0 
        self.fitness = 0 
        self.usedLeft = False 
        self.leftCount = 0 
        self.usedRight = False 
        self.rightCount = 0 
        self.usedShoot = False 
        
        # Network 
        self.network = Network(9, 9, 6, 3) 
        
        # Assets 
        self.playerShip = Ship() 
        self.ship_list = pygame.sprite.Group() 
        self.ship_list.add(self.playerShip) 
        
        self.asteroid_list = pygame.sprite.Group() 
        
        self.last_shot = 0 
        self.firerate = 200 
        self.bullet_list = pygame.sprite.Group() 
        
        self.los = []
        
    # Functions 
    def getStatus(self): 
        return self.gameOver 
    
    def getScore(self): 
        return self.score 
    
    def getShip(self): 
        return self.playerShip
        
    def getShipImg(self): 
        return self.playerShip.getImg() 
    
    
    def getShipRect(self): 
        return self.playerShip.getRect() 
    
    def shipMove(self, direction): 
        if direction == 0: 
            self.playerShip.rotate("left") 
            self.usedLeft = True 
            self.leftCount += 1
        if direction == 1: 
            self.playerShip.rotate("right") 
            self.usedRight = True 
            self.rightCount += 1 
            
    def spawnAsteroid(self): 
        side = np.random.randint(0, 4) # Left = 0, Right = 1, Top = 2, Bottom = 3
        if side == 0: 
            xPos = 0
            yPos = np.random.randint(0, 501) 
        elif side == 1: 
            xPos = 700
            yPos = np.random.randint(0, 501) 
        elif side == 2: 
            xPos = np.random.randint(0, 701) 
            yPos = 0 
        elif side == 3: 
            xPos = np.random.randint(0, 701) 
            yPos = 500 

        speed = np.random.randint(1, 4)
        
        asteroid = Asteroid(xPos, yPos, speed) 
        self.asteroid_list.add(asteroid) 
        
    def getAstList(self): 
        return self.asteroid_list
    
    def getBltList(self): 
        return self.bullet_list 
    
    def fire(self, time): 
        self.usedShoot = True 
        if(time >= self.last_shot + self.firerate or self.last_shot == 0): 
            self.last_shot = time
            
            center = self.playerShip.getORect().center 
            top = (self.playerShip.getORect()).top 
            
            radius = center[1] - top 
            
            posX = center[0]
            posY = center[1] 
            
            angle = self.playerShip.getAngle() 
            
            dx = radius * math.sin(math.radians(angle)) 
            dy = radius * math.cos(math.radians(angle)) 
            
            posX += dx 
            posY -= dy 
            
            bullet = Bullet(posX, posY, angle) 
            self.bullet_list.add(bullet) 
        
        
    # Destroy all assets in population 
    def nuke(self): 
        for plr in self.ship_list: 
            plr.destroy() 
        for ast in self.asteroid_list: 
            ast.destroy() 
        for blt in self.bullet_list: 
            blt.destroy() 
            
    
    def genVision(self, surface): 
        angle = 0 
        for i in range(0, 8): 
            self.los.append(Vision(surface, angle))
            angle += 45
            
    def getLos(self): 
        return self.los 
    
    # Returns distance from player of closest asteroid 
    # The closer it is, the larger the output
    def astDistance(self, astList): 
        xCenter = 700/2 
        yCenter = 500/2 
        furthestPoint = math.sqrt(math.pow(xCenter - 0, 2) + math.pow(yCenter - 0, 2))
        minDistance = 10000
        
        for ast in astList: 
            distance = math.sqrt(math.pow(ast.xPos - xCenter, 2) + math.pow(ast.yPos - yCenter, 2))
            if distance < minDistance: 
                minDistance = distance
        
        return furthestPoint - minDistance 
    
    def runNetwork(self, input_list): 
        outputs = self.network.get_outputs(input_list) 
        
        return outputs 
    
    def updateFitness(self): 
        strategy = 1
        
        if strategy == 1: 
            self.fitness = (self.score * 100) + (self.timeAlive / 100) 
            if self.usedShoot == True: 
                self.fitness += 5000000
            if self.usedLeft == True and self.usedRight == True: 
                self.fitness += 1000000
            elif self.usedLeft == True or self.usedRight == True: 
                self.fitness += 10000
                
            if self.usedLeft == True and self.usedRight == True and self.usedShoot == True: 
                self.fitness += 100000000000 
            
            if self.usedLeft == True and self.usedRight == True and (self.timeAlive / 1000 >= 15): 
                if self.leftCount >= self.rightCount: 
                    if (self.rightCount / self.leftCount) >= 0.6: 
                        self.fitness += 100000000000
                elif self.rightCount >= self.leftCount: 
                    if (self.leftCount / self.rightCount) >= 0.6: 
                        self.fitness += 100000000000 
                
            score_lim = 20 
            while int(self.score/20) >= score_lim: 
                self.fitness += 1000000 
                score_lim += 20 
        
        
        if strategy == 2: 
            self.fitness = (self.score + self.timeAlive) 
        