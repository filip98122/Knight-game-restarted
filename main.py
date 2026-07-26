from loader import *
ltexturesoffset={"attack":[[0,0],[42,0],[54,0],[0,0],[0,82]],"jump":[[0,0],[0,18],[0,0],[20,49],[0,46],[0,44]],"powerattack":[[14,0],[24,0],[14,55],[13,45]]}

def get_knight_rect(spritename:str,xleft:int,time:int,dirrectionr):
    if spritename in ltexturesoffset:
        if dirrectionr:
            newleft=xleft+ltexturesoffset[spritename][time][0]*scale
            newwidth=textures[f"Knightr{spritename}{time}"].get_width()-ltexturesoffset[spritename][time][1]*scale-ltexturesoffset[spritename][time][0]*scale
        else:
            newleft=xleft-ltexturesoffset[spritename][time][0]*scale
            newwidth=textures[f"Knightr{spritename}{time}"].get_width()-ltexturesoffset[spritename][time][1]*scale-ltexturesoffset[spritename][time][0]*scale
    else:
        if dirrectionr:
            newleft=xleft
            newwidth=textures[f"Knightr{spritename}{time}"].get_width()
        else:
            newwidth=textures[f"Knightr{spritename}{time}"].get_width()
            newleft=xleft
            
    return newleft,newwidth

def rectlinecolison(linecords:list,rectlike:pygame.Rect):
    if rectlike.clipline(linecords[0],linecords[1],linecords[2],linecords[3]):
        return True
    else:
        return False
    
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
        window.blit(s.scaled,(s.x+camerax,s.y+cameray))
    def ifplayerontop(s,px,py,pwidth,dirr):
        if dirr:
            if not (px>s.x+s.width+camerax):
                if not (px+pwidth<s.x+camerax) and py<s.y+cameray:
                    zadniji=False
                    if s.x+camerax>centerofmass:
                        zadniji="l"
                    if centerofmass>s.x+s.width+camerax:
                        zadniji="r"
                    return [True,s.y,s.x,s.width,zadniji]
            return [False,-1,-1,-1,None]
        else:
            if not (px-pwidth>s.x+camerax+s.width):
                if not (px<s.x+camerax) and py<s.y+cameray:
                    zadniji=False
                    if s.x+camerax>centerofmass:
                        zadniji="l"
                    if centerofmass>s.x+s.width+camerax:
                        zadniji="r"
                    return [True,s.y,s.x,s.width ,zadniji]
            return [False,-1,-1,-1,None]
        
lplatforms=[Platforms(1,0,HEIGHT-99,WIDTH//2-100,99),Platforms(1,WIDTH//2+100,HEIGHT-199,WIDTH//2-100,99),Platforms(1,0,HEIGHT-379,WIDTH//2-100,99),Platforms(1,WIDTH//2+100,HEIGHT-479,WIDTH//2-100,99)]




lskeletonspearmanlistofsprites={"attack":[(46, 0, 15, 17),(46, 0, 15, 17),(30, 0, 15, 17),(30, 0, 15, 17)],
                                "defend":[(20, 10, 15, 17), (10, 12, 15, 17)],
                                "defended":[(13, 0, 15, 17), (36, 0, 15, 17), (30, 0, 15, 17), (23, 0, 15, 17), (23, 0, 15, 17), (27, 28, 15, 17)],
                                "hurt":[(22, 33, 15, 17), (20, 28, 15, 17), (12, 23, 15, 17)],
                                "idle":[(15, 23, 15, 17), (15, 24, 15, 17), (15, 23, 15, 17), (15, 24, 15, 17), (15, 25, 15, 17), (15, 24, 15, 17), (15, 23, 15, 17)],
                                "run":[(52, 0, 15, 17), (48, 2, 15, 17), (48, 2, 15, 17), (52, 2, 15, 17), (48, 2, 15, 17), (52, 0, 15, 17)],
                                "runattack":[(46, 0, 15, 17), (46, 0, 15, 17), (30, 0, 15, 17), (30, 0, 15, 17), (30, 0, 15, 17)],
                                "walk":[(20, 28, 15, 17), (17, 28, 15, 17), (15, 27, 15, 17), (20, 28, 15, 17), (15, 27, 15, 17), (32, 26, 15, 17), (28, 25, 15, 17)]}





debugmodeforvision=False
holdingv=False


def angle_to_vector_unit_circle(angle):
    rad=math.radians(angle)
    dx=round(math.cos(rad),10)
    dy=round(math.sin(rad),10)
    return dx,dy

class Skeleton_spearman:
    def __init__(s,x,y,health,time,dirr,atributes=None):
        s.x=x
        s.y=y
        s.health=health
        s.time=time
        s.dirr=dirr
        s.state="stationary"
    def getheadpos(s):
        things=s.get_img()
        if s.dirr:
            dire="r"
        else:
            dire="l"
            
        cheight=textures[f"Skeletonspearman{dire}{things[0]}{things[-1]}"].get_height()
        if s.dirr:
            return s.x+skeletonscale*lskeletonspearmanlistofsprites[things[0]][things[-1]][0]+camerax,s.y+skeletonscale*lskeletonspearmanlistofsprites[things[0]][things[-1]][1]-cheight+cameray,skeletonscale*lskeletonspearmanlistofsprites[things[0]][things[-1]][2],skeletonscale*lskeletonspearmanlistofsprites[things[0]][things[-1]][3],things
        else:
            return s.x-skeletonscale*lskeletonspearmanlistofsprites[things[0]][things[-1]][0]+camerax,s.y+skeletonscale*lskeletonspearmanlistofsprites[things[0]][things[-1]][1]-cheight+cameray,skeletonscale*lskeletonspearmanlistofsprites[things[0]][things[-1]][2],skeletonscale*lskeletonspearmanlistofsprites[things[0]][things[-1]][3],things    
    def ray_cast_detetion(s):
        obrnuto=1
        if not s.dirr:
            obrnuto=-1
        
        
        headx,heady,headw,headh,things=s.getheadpos()# WITH camerax/y
        if s.dirr:
            angle=150
            endangle=213 #last angle is 210
        else:
            angle=327
            endangle=390
        halflife=HEIGHT//(HEIGHT//400)
        while True:
            color=(203,203,203)
            if angle==endangle:
                break
            dx,dy=angle_to_vector_unit_circle(angle)
            for i in range(len(lplatforms)):
                if rectlinecolison([headx+(headw//2*obrnuto),heady+(headh//2*obrnuto),headx+dx*halflife+(headw//2*obrnuto),heady+dy*halflife+(headh//2*obrnuto)],pygame.rect.Rect(lplatforms[i].x+camerax,lplatforms[i].y+cameray,lplatforms[i].width,lplatforms[i].height)):
                    color=(255,0,0)
            if color==(203,203,203):
                pass
                #Check player collision
            if debugmodeforvision:
                pygame.draw.rect(window,(0,255,0),pygame.rect.Rect(headx,heady,headw,headh))
                pygame.draw.line(window,(color),(headx+(headw//2*obrnuto),heady+(headh//2*obrnuto)),(headx+dx*halflife+(headw//2*obrnuto),heady+dy*halflife+(headh//2*obrnuto)))
            angle+=3
    def behaviour(s):
        pass
    def get_animation(s):
        
    
    

        if s.state=="stationary":
            spriitename="idle"
        return spriitename
    def get_img(s):   #Need to reset time after calling
        #Animation
        #Animation
        #Animation
        spritename=s.get_animation()
        #Direction
        #Direction
        #Direction
        #Direction
        if s.dirr:
            dire="r"
        else:
            dire="l"
        #Index
        #Index
        #Index
        amount=spritelistskeleton[spritename][0]
        timeamount=spritelistskeleton[spritename][1]
        #BLITING
        #BLITING
        #BLITING
        #BLITING
        s.time+=1
        s.time%=timeamount
        frame=int(s.time//(timeamount/amount))
        img=textures[f"Skeletonspearman{dire}{spritename}{frame}"]
        return [spritename,img,timeamount,amount,frame]
    def draw(s):
        things=s.get_img()
        if s.dirr:
            dire="r"
            window.blit(textures[f"Skeletonspearman{dire}{things[0]}{things[-1]}"],(s.x+camerax,s.y+cameray-textures[f"Skeletonspearman{dire}{things[0]}{things[-1]}"].get_height()))

        else:
            dire="l"
            window.blit(textures[f"Skeletonspearman{dire}{things[0]}{things[-1]}"],(s.x+camerax-textures[f"Skeletonspearman{dire}{things[0]}{things[-1]}"].get_width(),s.y+cameray-textures[f"Skeletonspearman{dire}{things[0]}{things[-1]}"].get_height()))

class Portrait:
    def __init__(s,x,y,portrait,offw,offh):
        s.x,s.y=x,y
        s.portrait=portrait
        s.offw,s.offh=offw,offh
        s.framewidth=textures["frame"].get_width()
        s.frameheight=textures["frame"].get_height()
        s.n90degeres=math.radians(90)
    def draw(s):
        window.blit(textures[s.portrait],(s.x+s.offw,s.y+s.offh))
        window.blit(textures["frame"],(s.x,s.y))
    def draw_hearts(s,maxh,h):
        if maxh>=h:
            xaddon=s.framewidth
            count=h//1
            for i in range(int(count)):
                window.blit(textures["heartf"],(s.x+xaddon,s.y+s.frameheight//10))
                xaddon+=textures["heartf"].get_width()+textures["heartf"].get_width()//7.5
            if h%1!=0:
                window.blit(textures["hearth"],(s.x+xaddon,s.y+s.frameheight//10))
                xaddon+=textures["hearth"].get_width()+textures["hearth"].get_width()//7.5
            for i in range(int(maxh-h)):
                window.blit(textures["heart3"],(s.x+xaddon,s.y+s.frameheight//10))
                xaddon+=textures["heart3"].get_width()+textures["heart3"].get_width()//7.5
    def draw_stamina(s,maxstamina,stamina):
        if maxstamina>=stamina:
            xaddon=s.framewidth+staminacirclediameter
            arcs=math.ceil(maxstamina//360)
            for i in range(arcs):
                pygame.draw.circle(window,(46, 230, 137), (s.x+xaddon,s.y+s.frameheight//2), int(staminacirclediameter//2.1),int(staminacirclediameter//3.5))
                pygame.draw.arc(window,(0,0,0),pygame.Rect(s.x+xaddon-staminacirclediameter//2,s.y+s.frameheight//2-staminacirclediameter//2,staminacirclediameter,staminacirclediameter),
                                s.n90degeres,math.radians(((stamina-90)%361)*-1+360),int(staminacirclediameter//2.9))
                stamina-=360
 
offsetportraitplayerw=(WIDTH/knighheadscale[0]-WIDTH/knighheadscale[2])/2
offsetportraitplayerh=(HEIGHT/knighheadscale[1]-HEIGHT/knighheadscale[3])/2
playerportrait=Portrait(0,0,"Knighttopright",offsetportraitplayerw,offsetportraitplayerh)
lskeletonsspearman=[Skeleton_spearman(WIDTH//2+100+WIDTH//4-50,HEIGHT-200,10,0,True)]
camerax,cameray=0,0

class Knight:
    def __init__(s,x,y,health,maxhealth,stamina,maxstamina,time,dirr,atributes=None):
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
        s.since_shift=0
        s.jumpspeedboost=1
        s.maxhealth=maxhealth
        s.jumped=False
    def move(s,keys,mouse,platy,sliding,camerax,cameray):
        if s.lockin==None:
            if not s.lasttimefell:
                speedboost=1
                sprite=s.get_animation(keys,mouse)
                if keys[pygame.K_LSHIFT] and s.stamina>0 and sprite!="rest":
                        speedboost*=2
                        s.stamina-=1
                        s.since_shift=200
                        if not s.shift:
                            s.shift=True
                            s.time=0
                else:
                    if s.shift:
                        s.shift=False
                        s.time=0
                    if s.since_shift==0:
                        s.stamina+=2
                        s.stamina=min(s.stamina,s.maxstamina)
                if keys[pygame.K_d]:
                    camerax-=s.speed*speedboost
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
                    camerax+=s.speed*speedboost
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
                if s.slided==False:
                    if s.directionr:
                        camerax-=s.speed*s.jumpspeedboost                
                    else:
                        camerax+=s.speed*s.jumpspeedboost

        #LOCKINS
        #LOCKINS
        #LOCKINS
        #LOCKINS
        #LOCKINS
        if s.lockin=="runattack":
            if s.directionr:
                camerax-=s.speed*2
            else:
                camerax+=s.speed*2
        if s.lockin=="attack":
            if s.time<21:
                if s.directionr:
                    camerax-=s.speed
                else:
                    camerax+=s.speed
        
        if s.lockin=="jump":
                #s.stamina-=0.5
            if s.directionr:
                camerax-=s.speed*s.jumpspeedboost                
            else:
                camerax+=s.speed*s.jumpspeedboost
                
                #ANIMATION
                #ANIMATION
                #ANIMATION
                #ANIMATION
                #ANIMATION
                #ANIMATION
                #ANIMATION
                #ANIMATION
        if sliding[-1]!=False and s.slided==False and s.lockin==None and s.lasttimefell==False:
            s.slidof-=1
            if s.slidof==0:
                s.slided=True
                s.slidof=150
                notordered=s.get_img(keys,mouse)
                widthframe=notordered[1].get_width()
                if sliding[-1]=="r":
                    if s.directionr:
                        #s.x=sliding[0]+sliding[1]+1
                        camerax-=sliding[0]+sliding[1]+camerax+1-s.x
                    else:
                        #s.x=sliding[0]+sliding[1]+1+widthframe
                        camerax-=sliding[0]+sliding[1]+camerax+1+widthframe-s.x
                if sliding[-1]=="l":
                    if s.directionr:
                        #s.x=sliding[0]-1-widthframe
                        camerax+=s.x-(sliding[0]-1-widthframe)-camerax
                    else:
                        #s.x=sliding[0]-1
                        camerax+=s.x-(sliding[0]-1)-camerax
        else:
            s.slidof=150
        
                
                
                
                
        #Y
        #Y
        #Y
        if platy==None:
            if s.jumped==False:
                s.jumpspeedboost=1
                if keys[pygame.K_LSHIFT] and s.stamina>0:
                    s.jumpspeedboost=2
                s.jumped=True 
            s.ddy+=ddyforplayerchange
            s.ddy=min(ddycapforplayer,s.ddy)
            s.dy+=s.ddy
            s.lasttimefell=True
            
        else:
            if platy+cameray>s.y and platy+cameray>s.y+s.dy and platy+cameray-s.y>1 or platy+cameray<s.y and platy+cameray<s.y+s.dy:
                s.ddy+=ddyforplayerchange
                s.ddy=min(ddycapforplayer,s.ddy)
                s.dy+=s.ddy
                s.lasttimefell=True
            elif (platy+cameray>s.y and not platy+cameray>s.y+s.dy) or (platy+cameray>s.y and platy+cameray<s.y+s.dy):
                if s.lasttimefell:
                    s.jumped=False
                    s.lasttimefell=False
                    s.ddy=0
                    s.dy=0
                s.jumpspeedboost=1
            
                cameray-=(platy+cameray)-0.5-s.y
        cameray-=s.dy
        if not keys[pygame.K_LSHIFT]:
            s.since_shift=max(s.since_shift-1,0)
        return [camerax,cameray]
    def get_animation(s,keys,mouse):
        spritename="rest"
        if s.lockin!=None:
            spritename=s.lockin
        else:
            if (keys[pygame.K_d] or keys[pygame.K_a]) and not (keys[pygame.K_d] and keys[pygame.K_a]):
                spritename="walk"
            if keys[pygame.K_LSHIFT] and s.stamina>0 and (keys[pygame.K_d] or keys[pygame.K_a]) and not (keys[pygame.K_d] and keys[pygame.K_a]):
                spritename="run"
            if (keys[pygame.K_d] and keys[pygame.K_a]):
                spritename="rest"
            if mouse[0]==True and s.lasttimefell==False:
                s.time=0
                spritename="attack"
                s.lockin="attack"
            if keys[pygame.K_LSHIFT] and s.stamina>0 and mouse[0] and s.lasttimefell==False:
                s.time=0
                spritename="runattack"
                s.lockin="runattack"
            if s.lasttimefell==False:
                if keys[pygame.K_SPACE]:
                    s.dy=-8
                    s.ddy=0
                    s.time=0
                    if keys[pygame.K_LSHIFT] and s.stamina>0:
                        s.jumpspeedboost=2
                    spritename="jump"
                    s.lockin="jump"
                    s.jumped=True
            if s.lockin==None and s.lasttimefell:
                spritename="jump"
                s.time=88
            if s.slided:
                s.lockin=None
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
        for i in range(len(namesofspritesKnight)):
            if namesofspritesKnight[i][0]==spritename:
                amount=namesofspritesKnight[i][1]
                timeamount=namesofspritesKnight[i][2]
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
        img=textures[f"Knight{dire}{spritename}{frame}"]
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
                textureoffset=50* scale
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
        #newx,neww=get_knight_rect(spritename,s.x,frame,s.directionr)
        #if s.directionr:
        #    centerofmassx=newx+neww//2
        #else:
        #    centerofmassx=newx-neww//2
        
        
        
        
        #pygame.draw.circle(window,(46, 230, 137),(centerofmassx,s.y-int(HEIGHT//14.22666666666667)*2.5),int(WIDTH//68.28),int(WIDTH//(68.28*2)))
        return img
        
player=Knight(WIDTH//2-50,HEIGHT//2+100,3.5,10,360,360,0,True)
camerax=WIDTH//2-300
cameray=(HEIGHT//2-HEIGHT)+200
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
    if keys[pygame.K_v]:
        if not holdingv:
            debugmodeforvision=not debugmodeforvision
            holdingv=True
    else:
        holdingv=False        
    playerstandingonplatform=False
    things=player.get_img(keys,mouseclicked)
    platformy=None
    verdict=[False,None]
    klizanje=[None]
    #OF FRAME
    #OF FRAME
    #OF FRAME
    difference=None
    plx,plwidth=get_knight_rect(things[0],player.x,things[-1],player.directionr)
    if player.directionr:
        centerofmass=plx+plwidth//2
    else:
        centerofmass=plx-plwidth//2
    for i in range(len(lplatforms)):
        lplatforms[i].draw(window)
        verdict=lplatforms[i].ifplayerontop(plx,player.y,plwidth,player.directionr)
        if verdict[0]:
            if difference==None:
                playerstandingonplatform=True
                platformy=verdict[1]
                difference=platformy-player.y+cameray
            else:
                if verdict[1]+cameray-player.y<=difference:
                    playerstandingonplatform=True
                    platformy=verdict[1]
                    difference=platformy-player.y+cameray
        if verdict[-1]==False:
            klizanje=[False]
        elif klizanje[-1]!=False:
            if klizanje[-1]==None:
                klizanje=verdict[2:5]
            if klizanje[-1]=="r" and verdict[-1]=="l":
                klizanje=[False]
            if klizanje[-1]=="l" and verdict[-1]=="r":
                klizanje=[False]
    for i in range(len(lskeletonsspearman)):
        lskeletonsspearman[i].draw()
        lskeletonsspearman[i].ray_cast_detetion()
    camera=player.move(keys,mouseclicked,platformy,klizanje,camerax,cameray)
    camerax,cameray=camera[0],camera[1]
    drawn_img=player.draw(keys,mouseclicked)
    playerportrait.draw()
    playerportrait.draw_hearts(player.maxhealth,player.health)
    playerportrait.draw_stamina(player.maxstamina,player.stamina)
    pygame.display.update()
    lastframekeys=keys
    clock.tick(45)