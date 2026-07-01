import pygame
import os
import random
import math
import time
import json
import copy
pygame.init()
pygame.joystick.init()
pygame.mixer.init()
keys = pygame.key.get_pressed()
clock = pygame.time.Clock()
events=pygame.event.get()
WIDTH,HEIGHT = 1707,1067
window = pygame.display.set_mode((WIDTH,HEIGHT))
while True:
    window.fill("Blue")
    keys = pygame.key.get_pressed()
    events=pygame.event.get()
    pygame.display.update()
    clock.tick(120)