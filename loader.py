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
namesofsprites=[["attack",5,50],["rest",2,150],["run",7,60],["runattack",6,45],["walk",8,120],["powerattack",4,["chargeup",20,20,20]],["challenge",5,180],["jump",6,90]]
scale=HEIGHT/900
platformamount=1
def load():
    textures={}
    for i in range(len(namesofsprites)):
        for j in range(namesofsprites[i][1]):
            a=pygame.image.load(f"textures/{namesofsprites[i][0]}{j}.png")
            textures[f"r{namesofsprites[i][0]}{j}"]=pygame.transform.scale(a,(a.get_width()*scale,a.get_height()*scale))
            textures[f"l{namesofsprites[i][0]}{j}"]=pygame.transform.flip(textures[f"r{namesofsprites[i][0]}{j}"],True,False)
    for i in range(platformamount):
        textures[i+1]=pygame.image.load(f"textures/{i+1}.png")
    return textures
textures=load()