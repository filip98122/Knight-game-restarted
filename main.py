from loader import *
class Knight:
    def __init__(s,x,y,health,stamina,maxstamina,time,dirr,atributes=None):
        s.x=x
        s.y=y
        s.health=health
        s.stamina=stamina
        s.maxstamina=maxstamina        
        s.time=time
        s.directionr=dirr
        s.speed=0.5
        s.shift=False
    def move(s,keys):
        speedboost=1
        if keys[pygame.K_LSHIFT]:
            speedboost*=2
            s.stamina-=0.5
            if not s.shift:
                s.shift=True
                s.time=0
        else:
            if s.shift:
                s.shift=False
                s.time=0
            s.stamina+=1
        if keys[pygame.K_d]:
            s.x+=s.speed*speedboost
            if not s.directionr:
                s.directionr=not s.directionr
                s.time=0
        if keys[pygame.K_a]:
            s.x-=s.speed*speedboost
            if s.directionr:
                s.directionr=not s.directionr
                s.time=0
    def draw(s,keys):
        
        #Animation
        #Animation
        #Animation
        spritename="rest"

        if (keys[pygame.K_d] or keys[pygame.K_a]):
            spritename="walk"
        if keys[pygame.K_LSHIFT] and (keys[pygame.K_d] or keys[pygame.K_a]):
            spritename="run"
        #Direction
        #Direction
        #Direction
        #Direction
        if s.directionr:
            dire="r"
        else:
            dire="l"
        #Index
        #Index
        #Index
        for i in range(len(namesofsprites)):
            if namesofsprites[i][0]==spritename:
                amount=namesofsprites[i][1]
                break
        #BLITING
        #BLITING
        #BLITING
        #BLITING
        window.blit(textures[f"{dire}{spritename}{int(s.time//(90/amount))}"],
                    (s.x,
                     s.y-
                     textures[f"{dire}{spritename}{int(s.time//(90/amount))}"].get_height()
                     ))
        s.time+=1
        s.time%=90
        #pygame.draw.circle(window,(0,0,0),)
player=Knight(300,HEIGHT-100,10,360,360,0,True)
while True:
    window.fill("Blue")
    keys = pygame.key.get_pressed()
    events=pygame.event.get()
    
    player.move(keys)
    player.draw(keys)
    pygame.display.update()
    clock.tick(60)