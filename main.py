import numpy as np
import pygame
import screen
from car import Car

allDead = True
bestCar = None
gen = 0
BestDist = 0
pygame.init()
MaxDist = 16000

font = pygame.font.Font(pygame.font.get_default_font(), 36)


def generation():
    global bestCar
    global BestDist
    cars = []
    deadCars = []

    allDead = False
    
    # First generation uses 100 cars to speed things up 
    if gen != 0:
        for i in range(10):
            cars.append(Car([550,570]))
        for c in cars:
            if c != bestCar:
                c.changeWeights(bestCar.getWeights())
                c.train()
    else:
        for i in range(100):
            cars.append(Car([550,570]))

    while allDead == False:
        screen.screen.blit(pygame.image.load('track.png'), (0,0))
        text_surface = font.render(f'Generation {gen}',True, (0, 0, 0))
        screen.screen.blit(text_surface, (0,0))
        text_surface = font.render(f'Longest Distance {round(BestDist)}',True, (0, 0, 0))
        screen.screen.blit(text_surface, (0,40))
        
        # Only draws cars that are not dead
        # Cars die after a given number of movements
        for i in range(len(cars)):
            if cars[i].getAlive() and cars[i].movements < 8000:
                cars[i].update()
                cars[i].move()
                cars[i].draw(screen.screen)
            else:
                if cars[i] not in deadCars:
                    deadCars.append(cars[i])

        pygame.display.flip()

        if len(cars) == len(deadCars):
            allDead = True
        
    # Finds the best performing car
    if bestCar == None:
        bestCar = cars[0]
    for i in range(len(cars)):
        if cars[i].dist > bestCar.dist:
            bestCar = cars[i]
    BestDist = bestCar.dist
    



while screen.running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            screen.running = False
    screen.screen.blit(pygame.image.load('track.png'), (0,0))
    
    # Only will run when all cars of previous generation are dead
    if allDead == True and BestDist != MaxDist:
        
        generation()
        gen += 1
    if MaxDist == BestDist:
        text_surface = font.render(f'Generation {gen}',True, (0, 0, 0))
        screen.screen.blit(text_surface, (0,0))
        text_surface = font.render(f'Longest Distance {round(BestDist)}',True, (0, 0, 0))
        screen.screen.blit(text_surface, (0,40))
        text_surface = font.render(f'Max Distance Reached',True, (0, 0, 0))
        screen.screen.blit(text_surface, (600,350))

    pygame.display.flip()