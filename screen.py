import pygame
(width, height) = (1280, 720)
running = True
screen = pygame.display.set_mode((width, height))
screen.blit(pygame.image.load('track.png'), (0,0))

pygame.display.flip()