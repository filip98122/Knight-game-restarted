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
namesofsprites=[["attack",5,50],["rest",2,150],["run",7,60],["runattack",6,45],["walk",8,120],["powerattack",4,["chargeup",20,20,20]],["challenge",5,180],["jump",6,90],["falling",1,60]]
scale=HEIGHT/900
platformamount=1
knighheadscale=[4.962209302325581,3.066091954022989,6.654970760233918,4.1598440545808970]
for i in range(4):
    knighheadscale[i]*=2
def load():
    textures={}
    for i in range(len(namesofsprites)):
        for j in range(namesofsprites[i][1]):
            a=pygame.image.load(f"textures/Knight/{namesofsprites[i][0]}{j}.png")
            textures[f"Knightr{namesofsprites[i][0]}{j}"]=pygame.transform.scale(a,(a.get_width()*scale,a.get_height()*scale))
            textures[f"Knightl{namesofsprites[i][0]}{j}"]=pygame.transform.flip(textures[f"Knightr{namesofsprites[i][0]}{j}"],True,False)
    for i in range(platformamount):
        textures[i+1]=pygame.image.load(f"textures/Platforms/{i+1}.png")
    textures["frame"]=pygame.transform.scale(pygame.image.load("textures/portraits/frame344348.png"),(WIDTH/knighheadscale[0],HEIGHT/knighheadscale[1]))
    textures["Knighttopright"]=pygame.transform.scale(pygame.image.load("textures/portraits/Knighttopright.png"),(WIDTH/knighheadscale[2],HEIGHT/knighheadscale[3]))
    return textures
textures=load()