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
namesofspritesKnight=[["attack",5,50],["rest",2,150],["run",7,60],["runattack",6,45],["walk",8,120],["powerattack",4,["chargeup",20,20,20]],["challenge",5,180],["jump",6,90],["falling",1,60]]
scale=HEIGHT/900
platformamount=1
knighheadscale=[4.962209302325581,3.066091954022989,6.654970760233918,4.1598440545808970]
heartchange=WIDTH/(5257.56*2)
staminacirclediameter=HEIGHT//21.34
lhearts=["f","3","h"]
spritelistskeleton={"idle":[7,250]}
skeletonscale=HEIGHT/(HEIGHT/2)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
import queue
for i in range(4):
    knighheadscale[i]*=2
def load():
    textures={}
    for i in range(len(namesofspritesKnight)):
        for j in range(namesofspritesKnight[i][1]):
            scale=HEIGHT/900
            a=pygame.image.load(f"textures/Knight/{namesofspritesKnight[i][0]}{j}.png")
            textures[f"Knightr{namesofspritesKnight[i][0]}{j}"]=pygame.transform.scale(a,(a.get_width()*scale,a.get_height()*scale))
            textures[f"Knightl{namesofspritesKnight[i][0]}{j}"]=pygame.transform.flip(textures[f"Knightr{namesofspritesKnight[i][0]}{j}"],True,False)
    for i in range(platformamount):
        textures[i+1]=pygame.image.load(f"textures/Platforms/{i+1}.png")
    textures["frame"]=pygame.transform.scale(pygame.image.load("textures/portraits/frame344348.png"),(WIDTH/knighheadscale[0],HEIGHT/knighheadscale[1]))
    textures["Knighttopright"]=pygame.transform.scale(pygame.image.load("textures/portraits/Knighttopright.png"),(WIDTH/knighheadscale[2],HEIGHT/knighheadscale[3]))
    for i in range(len(lhearts)):
        a=pygame.image.load(f"textures/icons/heart{lhearts[i]}.png")
        textures[f"heart{lhearts[i]}"]=pygame.transform.scale(a,(a.get_width()*heartchange,a.get_height()*heartchange))
    for i in spritelistskeleton:
        for j in range(spritelistskeleton[i][0]):
            a=pygame.image.load(f"textures/Skeleton/{i}{j}.png")
            textures[f"Skeletonspearmanr{i}{j}"]=pygame.transform.scale(a,(a.get_width()*skeletonscale,a.get_height()*skeletonscale))
            textures[f"Skeletonspearmanl{i}{j}"]=pygame.transform.flip(textures[f"Skeletonspearmanr{i}{j}"],True,False)
    
    return textures
textures=load()