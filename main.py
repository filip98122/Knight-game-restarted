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
        s.speed=3
        s.shift=False
        s.previousanimation=None
        s.lockin=None
    def move(s,keys,mouse):
        speedboost=1
        
        if keys[pygame.K_LSHIFT]  and s.lockin==None:
            speedboost*=2
            s.stamina-=0.5
            if not s.shift:
                s.shift=True
                s.time=0
        elif s.lockin==None:
            if s.shift:
                s.shift=False
                s.time=0
            s.stamina+=1
        if keys[pygame.K_d] and s.lockin==None:
            s.x+=s.speed*speedboost
            if not s.directionr:
                s.directionr=not s.directionr




                spritename=s.get_animation(keys,mouse)
                if s.directionr:
                    dire="r"
                else:
                    dire="l"
                for i in range(len(namesofsprites)):
                    if namesofsprites[i][0]==spritename:
                        amount=namesofsprites[i][1]
                        timeamount=namesofsprites[i][2]
                        break
                img=textures[f"{dire}{spritename}{int(s.time//(timeamount/amount))}"]
                s.x-=img.get_width()
                
                
                
                #s.time=0
        if keys[pygame.K_a] and s.lockin==None:
            s.x-=s.speed*speedboost
            if s.directionr:
                s.directionr=not s.directionr
                
                
                
                spritename=s.get_animation(keys,mouse)
                if s.directionr:
                    dire="r"
                else:
                    dire="l"
                for i in range(len(namesofsprites)):
                    if namesofsprites[i][0]==spritename:
                        amount=namesofsprites[i][1]
                        timeamount=namesofsprites[i][2]
                        break
                img=textures[f"{dire}{spritename}{int(s.time//(timeamount/amount))}"]
                s.x+=img.get_width()
                
                
                #s.time=0
        if s.lockin=="runattack":
            if s.directionr:
                s.x+=s.speed*2
            else:
                s.x-=s.speed*2
        if s.lockin=="attack":
            if s.time<21:
                if s.directionr:
                    s.x+=s.speed
                else:
                    s.x-=s.speed
    def get_animation(s,keys,mouse):
        spritename="rest"
        if s.lockin!=None:
            spritename=s.lockin
        else:
            if (keys[pygame.K_d] or keys[pygame.K_a]):
                spritename="walk"
            if keys[pygame.K_LSHIFT] and (keys[pygame.K_d] or keys[pygame.K_a]):
                spritename="run"
            if mouse[0]==True:
                s.time=0
                spritename="attack"
                s.lockin="attack"
            if keys[pygame.K_LSHIFT] and mouse[0]:
                s.time=0
                spritename="runattack"
                s.lockin="runattack"
        return spritename
    def draw(s,keys,mouse):
        
        #Animation
        #Animation
        #Animation
        spritename=s.get_animation(keys,mouse)
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
                timeamount=namesofsprites[i][2]
                break
        #BLITING
        #BLITING
        #BLITING
        #BLITING
        s.time+=1
        if s.lockin!=None:
            if s.time>=timeamount:
                s.lockin=None
                spritename=s.get_animation(keys,mouse)
        if spritename!=s.previousanimation and s.lockin==None:
            s.time=0

        s.time%=timeamount
        img=textures[f"{dire}{spritename}{int(s.time//(timeamount/amount))}"]
        textureoffset=0
        if spritename=="attack":
            if int(s.time//(timeamount/amount))==1:
                textureoffset=26*scale
            elif int(s.time//(timeamount/amount))==2:
                textureoffset=50*scale
        textureoffset=int(textureoffset)
        if s.directionr:
            #26
            #50
            window.blit(img,
                    (s.x-textureoffset,
                     s.y-
                     img.get_height()
                     ))
        else:
            window.blit(img,
                    (s.x-
                     img.get_width()+
                     textureoffset,
                     s.y-
                     img.get_height()
                     ))
        s.previousanimation=copy.deepcopy(spritename)
        #pygame.draw.circle(window,(0,0,0),)
player=Knight(300,HEIGHT-100,10,360,360,0,True)
while True:
    window.fill("Blue")
    keys = pygame.key.get_pressed()
    mousepos=pygame.mouse.get_pos()
    mouseclicked=pygame.mouse.get_pressed()
    events=pygame.event.get()
    for ev in events:
        if ev.type==pygame.QUIT:
            break
    
    if keys[pygame.K_ESCAPE]:
        break
    player.move(keys,mouseclicked)
    player.draw(keys,mouseclicked)
    pygame.display.update()
    clock.tick(60)