from loader import *
ltexturesoffset={"attack":[[0,0],[42,0],[54,0],[0,0],[0,82]],"jump":[[0,0],[0,18],[0,0],[20,49],[0,46],[0,44]],"powerattack":[[14,0],[24,0],[14,55],[13,45]]}

def get_knight_rect(spritename:str,xleft:int,time:int):
    if spritename in ltexturesoffset:
        newleft=xleft+ltexturesoffset[spritename][time][0]*scale
        newwidth=textures[f"r{spritename}{time}"].get_width()-ltexturesoffset[spritename][time][1]*scale
    else:
        newleft=xleft
        newwidth=textures[f"r{spritename}{time}"].get_width()
    return newleft,newwidth



ddyforplayerchange=HEIGHT/53350
ddycapforplayer=HEIGHT/5335
class Platforms:
    def __init__(s,pic:int,x,y,width,height):
        s.x=x
        s.y=y
        s.width=width
        s.height=height
        s.scaled=pygame.transform.scale(textures[pic],(s.width,s.height))
        s.pic=pic
        
    def draw(s,window):
        window.blit(s.scaled,(s.x,s.y))
    def ifplayerontop(s,px,py,pwidth,dirr):
        if dirr:
            if not (px>s.x+s.width):
                if not (px+pwidth<s.x) and py<s.y:
                    zadniji=False
                    if s.x>centerofmass:
                        zadniji="l"
                    if centerofmass>s.x+s.width:
                        zadniji="r"
                    return [True,s.y,s.x,s.width,zadniji]
            return [False,-1,-1,-1,None]
        else:
            if not (px-pwidth>s.x+s.width):
                if not (px<s.x) and py<s.y:
                    zadniji=False
                    if s.x>centerofmass:
                        zadniji="l"
                    if centerofmass>s.x+s.width:
                        zadniji="r"
                    return [True,s.y,s.x,s.width ,zadniji]
            return [False,-1,-1,-1,None]
        
lplatforms=[Platforms(1,0,HEIGHT-99,WIDTH//2-100,99),Platforms(1,WIDTH//2+100,HEIGHT-199,WIDTH//2-100,99),Platforms(1,0,HEIGHT-379,WIDTH//2-100,99),Platforms(1,WIDTH//2+100,HEIGHT-479,WIDTH//2-100,99)]
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
        s.dy=0
        s.ddy=0
        s.slidof=300
        s.lasttimefell=False
        s.slided=False
    def move(s,keys,mouse,platy,sliding):
        if s.lockin==None:
            if not s.lasttimefell:
                speedboost=1
                s.jumpspeedboost=1
                if keys[pygame.K_LSHIFT]:
                    speedboost*=2
                    #s.stamina-=0.5
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

                        #SIDE CHANGE
                        #SIDE CHANGE
                        #SIDE CHANGE
                        #SIDE CHANGE
                        g=s.get_img(keys,mouse)
                        img=g[1]
                        s.x-=img.get_width()
                        s.time-=1
                    
                if keys[pygame.K_a]:
                    s.x-=s.speed*speedboost
                    if s.directionr:
                        s.directionr=not s.directionr
                        
                        #SIDE CHANGE
                        #SIDE CHANGE
                        #SIDE CHANGE
                        #SIDE CHANGE
                        g=s.get_img(keys,mouse)
                        img=g[1]
                        s.x+=img.get_width()
                        s.time-=1
            else:
                if s.directionr:
                    s.x+=s.speed*s.jumpspeedboost                
                else:
                    s.x-=s.speed*s.jumpspeedboost

        #LOCKINS
        #LOCKINS
        #LOCKINS
        #LOCKINS
        #LOCKINS
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
        
        if s.lockin=="jump":
                #s.stamina-=0.5
            if s.directionr:
                s.x+=s.speed*s.jumpspeedboost                
            else:
                s.x-=s.speed*s.jumpspeedboost
                
                #ANIMATION
                #ANIMATION
                #ANIMATION
                #ANIMATION
                #ANIMATION
                #ANIMATION
                #ANIMATION
                #ANIMATION
        if sliding[-1]!=False:
            s.slidof-=1
            if s.slidof==0:
                s.slided=True
                s.slidof=300
                if sliding[-1]=="r":
                    s.x=sliding[0]+sliding[1]+1
                if sliding[-1]=="l":
                    s.x=sliding[0]-1
        else:
            s.slidof=300
        
                
                
                
                
        #Y
        #Y
        #Y
        if platy==None:
            s.ddy+=ddyforplayerchange
            s.ddy=min(ddycapforplayer,s.ddy)
            s.dy+=s.ddy
            s.lasttimefell=True
            
        else:
            if platy>s.y and platy>s.y+s.dy and s.y-platy!=-1 or platy<s.y and platy<s.y+s.dy:
                s.ddy+=ddyforplayerchange
                s.ddy=min(ddycapforplayer,s.ddy)
                s.dy+=s.ddy
                s.lasttimefell=True
            elif (platy>s.y and not platy>s.y+s.dy) or (platy>s.y and platy<s.y+s.dy):
                if s.lasttimefell:
                    s.lasttimefell=False
                    s.ddy=0
                    s.dy=0
            
                s.y=platy-1
        s.y+=s.dy
    def get_animation(s,keys,mouse):
        spritename="rest"
        if s.lockin!=None:
            spritename=s.lockin
        else:
            if (keys[pygame.K_d] or keys[pygame.K_a]) and not (keys[pygame.K_d] and keys[pygame.K_a]):
                spritename="walk"
            if keys[pygame.K_LSHIFT] and (keys[pygame.K_d] or keys[pygame.K_a]) and not (keys[pygame.K_d] and keys[pygame.K_a]):
                spritename="run"
            if (keys[pygame.K_d] and keys[pygame.K_a]):
                spritename="rest"
            if mouse[0]==True:
                s.time=0
                spritename="attack"
                s.lockin="attack"
            if keys[pygame.K_LSHIFT] and mouse[0]:
                s.time=0
                spritename="runattack"
                s.lockin="runattack"
            if s.lasttimefell==False:
                if keys[pygame.K_SPACE]:
                    s.dy=-8
                    s.ddy=0
                    s.time=0
                    if keys[pygame.K_LSHIFT]:
                        s.jumpspeedboost=2
                    spritename="jump"
                    s.lockin="jump"
            if s.lockin==None and s.lasttimefell:
                spritename="jump"
                s.time=88
            if s.slided:
                s.lockin==None
                s.time=0
                spritename="falling"
        return spritename
    
    def get_img(s,keys,mouse):
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
        frame=int(s.time//(timeamount/amount))
        img=textures[f"{dire}{spritename}{frame}"]
        return [spritename,img,timeamount,amount,frame]
    def draw(s,keys,mouse):
        notordered=s.get_img(keys,mouse)
        frame=notordered[4]
        amount=notordered[3]
        timeamount=notordered[2]
        img=notordered[1]
        spritename=notordered[0]
        
        textureoffset=0
        if spritename=="attack":
            if frame==1:
                textureoffset=26*scale
            elif frame==2:
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
lastframekeys=[]
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
    playerstandingonplatform=False
    things=player.get_img(keys,mouseclicked)
    platformy=None
    verdict=[False,None]
    klizanje=[None]
    #OF FRAME
    #OF FRAME
    #OF FRAME
    difference=None
    plx,plwidth=get_knight_rect(things[0],player.x,things[-1])
    centerofmass=plx+plwidth//2
    for i in range(len(lplatforms)):
        lplatforms[i].draw(window)
        verdict=lplatforms[i].ifplayerontop(plx,player.y,plwidth,player.directionr)
        if verdict[0]:
            if difference==None:
                playerstandingonplatform=True
                platformy=verdict[1]
                difference=platformy-player.y
            else:
                if verdict[1]-player.y<=difference:
                    playerstandingonplatform=True
                    platformy=verdict[1]
                    difference=platformy-player.y
        if verdict[-1]==False:
            klizanje=[False]
        elif klizanje[-1]!=False:
            if klizanje[-1]==None:
                klizanje=verdict[2:5]
            if klizanje[-1]=="r" and verdict[-1]=="l":
                klizanje=[False]
            if klizanje[-1]=="l" and verdict[-1]=="r":
                klizanje==[False]
            
    
    player.move(keys,mouseclicked,platformy,klizanje)
    player.draw(keys,mouseclicked)
    pygame.display.update()
    lastframekeys=keys
    clock.tick(45)