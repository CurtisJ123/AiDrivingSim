import pygame
import math
import numpy as np


def getAngle(inputs,weights):
    output = 0
    Neuron = 0
    for i in range(len(inputs)):
        Neuron += (inputs[i] * weights[i])
    output = Neuron * weights[6]

    
    return 1/(1+ np.exp(-output))

def getSpeed(inputs,weights):
    output = 0
    Neuron = 0
    for i in range(len(inputs)):
        Neuron += (inputs[i] * weights[i+6])
    output = Neuron * weights[11]

    
    return 1/(1+ np.exp(-output))

class Car:
    def __init__(self,pos):
        self.pos = pos
        self.surface = pygame.image.load('car.png')
        self.surface = pygame.transform.scale(self.surface,(100,100))

        self.rotate_surface = self.surface
        self.center = [self.pos[0] + 50, self.pos[1] + 50]
        self.angle = 0
        self.whiskers = []
        self.map = pygame.image.load('track.png')

        self.dist = 0

        self.four_points = []
        self.is_alive = True

        self.speed = 0

        self.weights = np.random.uniform(-1,1,12)
        self.learningRate = 0.5

        self.output = 0
        self.movements = 0

    def move(self):
        
        # self.speed += getSpeed(self.output, self.weights)
        # if self.speed < 1:
        #     self.speed = 1
        # elif self.speed > 4:
        #     self.speed = 4
        self.speed = 2
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        
        self.center = [self.pos[0] + 50, self.pos[1] + 50]
        
        angle = getAngle(self.output,self.weights)
        angle = (angle - 0.5) * 5

        self.angle += angle
        self.dist += self.speed
        self.movements += 1

    def check_collision(self, map):
        self.is_alive = True
        for i,p in enumerate(self.four_points):
            if map.get_at((int(p[0]), int(p[1]))) == (255, 255, 255, 255):
                self.is_alive = False
                
                break

    def getWeights(self):
        output = []
        for w in self.weights:
            output.append(w)
        return output

    def changeWeights(self,w):
        self.weights = w

    def getAlive(self):
        return self.is_alive
    
    def update(self):
        output = [0,0,0,0,0]
        self.rotate_surface = self.rot_center(self.surface,self.angle)

        self.whiskers.clear()
        for d in [-90,-45,0,45,90]:
            self.checkWhiskers(d)
        for i,w in enumerate(self.whiskers):
            output[i] = w[1]
        
        len = 40

        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * len]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * len]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * len]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * len]
        self.four_points = [left_top, right_top, left_bottom, right_bottom]
        

        self.check_collision(self.map)
        self.output = output
        
    def draw(self,screen):
        pygame.draw.circle(screen, (0, 255, 0), self.center, 5)
        screen.blit(self.rotate_surface,self.pos)
        self.drawWhiskers(screen)
        for p in self.four_points:
            pygame.draw.circle(screen, (0, 255, 0), p, 5)

    def drawWhiskers(self, screen):
        for r in self.whiskers:
            pos, dist = r
            pygame.draw.line(screen, (0, 255, 0), self.center, pos, 1)
            pygame.draw.circle(screen, (0, 255, 0), pos, 5)

    def checkWhiskers(self,degree):
        len = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

        while not self.map.get_at((x, y)) == (255, 255, 255, 255) and len < 500:
            len = len + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        #print(dist)
        self.whiskers.append([(x, y), dist])
    

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def train(self):
        for i in range(len(self.weights)):
            self.weights[i] += np.random.uniform(-1,1,1)[0] * self.learningRate