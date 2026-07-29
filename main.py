from loader import *
ltexturesoffset={"attack":[[0,0,0,0],[26,0,0,0],[50,0,0,0],[0,0,0,0],[0,82,0,0]],
                 "jump":[[0,0,0,0],[0,18,0,0],[0,0,0,0],[20,49,0,0],[0,46,0,0],[0,44,0,0]],
                 "powerattack":[[14,0],0,0,[24,0,0,0],[14,55,0,0],[13,45,0,0]],
                 "runattack":[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]}

def get_knight_rect(spritename:str,xleft:int,time:int,dirrectionr):
    textureoffset=0
    if spritename=="attack":
        if time==1:
            textureoffset=26*scale
        elif time==2:
            textureoffset=50* scale
    textureoffset=int(textureoffset)
    if spritename in ltexturesoffset:
        if dirrectionr:
            newleft=xleft+ltexturesoffset[spritename][time][0]*scale-textureoffset
            newwidth=textures[f"Knightr{spritename}{time}"].get_width()-ltexturesoffset[spritename][time][1]*scale-ltexturesoffset[spritename][time][0]*scale
        else:
            newleft=xleft-ltexturesoffset[spritename][time][0]*scale+textureoffset
            newwidth=textures[f"Knightr{spritename}{time}"].get_width()-ltexturesoffset[spritename][time][1]*scale-ltexturesoffset[spritename][time][0]*scale
    else:
        if dirrectionr:
            newleft=xleft-textureoffset
            newwidth=textures[f"Knightr{spritename}{time}"].get_width()
        else:
            newwidth=textures[f"Knightr{spritename}{time}"].get_width()
            newleft=xleft+textureoffset
            
    return newleft,newwidth

def rectlinecolison(linecords:list,rectlike:pygame.Rect):
    a=rectlike.clipline(linecords[0],linecords[1],linecords[2],linecords[3])
    if a:
        entry=a[0]
        x,y=entry[0],entry[1]
        return True,x,y
    else:
        return False,None,None
    
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
        
lplatforms=[Platforms(1,0,HEIGHT-99,WIDTH//2-100,99),
            Platforms(1,WIDTH//2+100,HEIGHT-199,WIDTH//2-100,99),
            Platforms(1,0,HEIGHT-379,WIDTH//2-100,99),
            Platforms(1,WIDTH//2+100,HEIGHT-479,WIDTH//2-100,99)]

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

class Enemy:
    def getheadpos(s,scale,dict):
        things=s.get_img()
        s.time-=1
        if s.dirr:
            dire="r"
        else:
            dire="l"
        cheight=textures[f"{type(s).__name__}{dire}{things[0]}{things[-1]}"].get_height()
        if s.dirr:
            return s.x+scale*dict[things[0]][things[-1]][0]+camerax,s.y+scale*dict[things[0]][things[-1]][1]-cheight+cameray,scale*dict[things[0]][things[-1]][2],scale*dict[things[0]][things[-1]][3],things
        else:
            return s.x-scale*dict[things[0]][things[-1]][0]+camerax,s.y+scale*dict[things[0]][things[-1]][1]-cheight+cameray,scale*dict[things[0]][things[-1]][2],scale*dict[things[0]][things[-1]][3],things
    def ray_cast_detetion(s,width,height,obr,scale,dict):
        headx,heady,headw,headh,things=s.getheadpos(scale,dict)# WITH camerax/y
        detected=False
        if not s.dirr:
            angle=150
            endangle=213 #last angle is 210
        else:
            angle=327
            endangle=390
        halflife=HEIGHT//(HEIGHT//400)
        if debugmodeforvision:
            pygame.draw.rect(window,(0,255,0),pygame.rect.Rect(headx-headw//2,heady-headh//2,headw,headh))
        while True:
            distance=float("inf")
            color=(255, 255, 0)
            if angle==endangle:
                break
            dx,dy=angle_to_vector_unit_circle(angle)
            for i in range(len(lplatforms)):
                a,b,c=rectlinecolison([headx,heady,headx+dx*halflife,heady+dy*halflife],pygame.rect.Rect(lplatforms[i].x+camerax,lplatforms[i].y+cameray,lplatforms[i].width,lplatforms[i].height))
                if a:
                    distance=math.sqrt(2**(abs(headx-b))+(abs(heady-c))**2)
                    color=(255,0,0)
            
            a2,b2,c2=rectlinecolison([headx,heady,headx+dx*halflife,heady+dy*halflife],pygame.rect.Rect(player.x+width*obrnuto,player.y-height,width,height))
            if a2:
                distance2=math.sqrt(2**(abs(headx-b2))+(abs(heady-c2))**2)
                if distance2<=distance:
                    color=(0,255,0)
                    detected=True
            #Check player collision
            if debugmodeforvision:
                pygame.draw.line(window,(color),(headx,heady),(headx+dx*halflife,heady+dy*halflife))
            angle+=3
        return detected
    def get_img(s):   #Need to reset time after calling
        #Animation
        spritename=s.get_animation()
        #Direction
        if s.dirr:
            dire="r"
        else:
            dire="l"
        #Index
        amount=spritelistskeleton[spritename][0]
        timeamount=spritelistskeleton[spritename][1]
        #BLITING
        s.time+=1
        s.time%=timeamount
        frame=int(s.time//(timeamount/amount))
        img=textures[f"{type(s).__name__}{dire}{things[0]}{things[-1]}"]
        return [spritename,img,timeamount,amount,frame]
    def draw(s):
        things=s.get_img()
        if s.dirr:
            dire="r"
            window.blit(things[1],(s.x+camerax,s.y+cameray-textures[f"Skeletonspearman{dire}{things[0]}{things[-1]}"].get_height()))

        else:
            dire="l"
            window.blit(things[1],(s.x+camerax-textures[f"Skeletonspearman{dire}{things[0]}{things[-1]}"].get_width(),s.y+cameray-textures[f"Skeletonspearman{dire}{things[0]}{things[-1]}"].get_height()))
class Node:
    def __init__(s,pos,neighbors,color):
        s.x,s.y=pos
        s.color=color
        s.neighbors=neighbors
lnodes=[]
def h(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2)+abs(y1-y2)


def algorithim(l,start,end):
    count=0
    startindex=l[start[0]+start[1]*50]
    endindex=l[end[0]+end[1]*50]
    openset=queue.PriorityQueue()
    openset.put((0,count,startindex))
    camefrom={}
    g_score={Node:float("inf") for Node in l}
    f_score={Node:float("inf") for Node in l}
    f_score[startindex]=h(start,end)
    g_score[startindex]=0
    opensethashforqueue={startindex}
    while not openset.empty():
        events=pygame.event.get()
        for event in events:
            if event.type==pygame.QUIT:
                pygame.quit()
        current=openset.get()[2]
        opensethashforqueue.remove(current)
        if current==endindex:
            count=0
            while True:
                if camefrom[current]==startindex:
                    break
                camefrom[current].color=TURQUOISE
                count+=1
                current=camefrom[current]
            return True #DONE
        for neighbor in current.neighbors:
            temp_g_score=g_score[current]+1     #PLUS ONE CAN BE WEIGHTED
            if temp_g_score<g_score[neighbor]:
                camefrom[neighbor]=current
                g_score[neighbor]=temp_g_score
                f_score[neighbor]=temp_g_score+h((neighbor.col,neighbor.row),end)
                if neighbor not in opensethashforqueue:
                    count+=1
                    openset.put((f_score[neighbor],count,neighbor))
                    opensethashforqueue.add(neighbor)
                    if l[neighbor.col*50+neighbor.row].color!=PURPLE and l[neighbor.col*50+neighbor.row].color!=ORANGE:
                        l[neighbor.col*50+neighbor.row].color=GREEN
        for i in range(len(l)):
            l[i].draw()
        if current!=start:
            if l[current.col*50+current.row].color!=PURPLE and l[current.col*50+current.row].color!=ORANGE:
                l[current.col*50+current.row].color=RED

    return False

class Skeletonspearman(Enemy):
    def __init__(s,x,y,health,time,dirr,state,atributes=None):
        s.x=x
        s.y=y
        s.health=health
        s.time=time
        s.dirr=dirr
        s.state=state
        s.sincedetection=0
    def behaviour(s,detected):
        if s.sincedetection<300:
            if detected:
                s.sincedetection=0
            else:
                s.sincedetection+=1
        else:
            if detected:
                s.state="hunting"
            elif s.state=="hunting":#BILO
                s.state="returning"
    def move(s):
        pass
    def get_animation(s):
        if s.state=="stationary":
            spriitename="idle"
        return spriitename



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
lskeletonsspearman=[Skeletonspearman(WIDTH//2+100+WIDTH//4-50,HEIGHT-200,10,0,True)]
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
                if keys[pygame.K_LSHIFT] and s.stamina>0 and sprite!="rest": #For boosting speed
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
                if keys[pygame.K_d]:#moving right
                    camerax-=s.speed*speedboost
                    if not s.directionr:
                        s.directionr=not s.directionr
                        #SIDE CHANGE
                        g=s.get_img(keys,mouse)
                        img=g[1]
                        s.x-=img.get_width()
                        s.time-=1
                if keys[pygame.K_a]:#moving left
                    camerax+=s.speed*speedboost
                    if s.directionr:
                        s.directionr=not s.directionr
                        #SIDE CHANGE
                        g=s.get_img(keys,mouse)
                        img=g[1]
                        s.x+=img.get_width()
                        s.time-=1
            else: #If not slided, move on x axis
                if s.slided==False:
                    if s.directionr:
                        camerax-=s.speed*s.jumpspeedboost                
                    else:
                        camerax+=s.speed*s.jumpspeedboost
        else:
            s.since_shift=200
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
            if s.directionr:
                camerax-=s.speed*s.jumpspeedboost                
            else:
                camerax+=s.speed*s.jumpspeedboost
                #ANIMATION
        if sliding[-1]!=False and s.slided==False and s.lockin==None and s.lasttimefell==False: #decreasing slidof
            s.slidof-=1
            if s.slidof==0:
                s.slided=True
                s.slidof=150
                notordered=s.get_img(keys,mouse)
                widthframe=notordered[1].get_width()
                if sliding[-1]=="r":
                    if s.directionr:
                        camerax-=sliding[0]+sliding[1]+camerax+1-s.x
                    else:
                        camerax-=sliding[0]+sliding[1]+camerax+1+widthframe-s.x
                if sliding[-1]=="l":
                    if s.directionr:
                        camerax+=s.x-(sliding[0]-1-widthframe)-camerax
                    else:
                        camerax+=s.x-(sliding[0]-1)-camerax
        else:#if not on the edge reset slidof
            s.slidof=150
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
        spritename=s.get_animation(keys,mouse)
        #Direction
        if s.directionr:
            dire="r"
        else:
            dire="l"
        #Index
        for i in range(len(namesofspritesKnight)):
            if namesofspritesKnight[i][0]==spritename:
                amount=namesofspritesKnight[i][1]
                timeamount=namesofspritesKnight[i][2]
                break
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
    difference=None
    if keys[pygame.K_b]:
        breakpoint()
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
    if player.directionr:
        diree="r"
        obrnuto=0
        obrnuto2=1
    else:
        diree="l"
        obrnuto=-1
        obrnuto2=-1
    for i in range(len(lskeletonsspearman)):
        detected=lskeletonsspearman[i].ray_cast_detetion(plwidth,things[1].get_height(),obrnuto,skeletonscale,lskeletonspearmanlistofsprites)
        lskeletonsspearman[i].draw()
    camera=player.move(keys,mouseclicked,platformy,klizanje,camerax,cameray)
    camerax,cameray=camera[0],camera[1]
    drawn_img=player.draw(keys,mouseclicked)
    playerportrait.draw()
    if debugmodeforvision:
        pygame.draw.circle(window,(0,255,0),(plx+plwidth//2*obrnuto2,player.y-things[1].get_height()//2),5)
        #pygame.draw.rect(window,(0,255,0),pygame.Rect(plx+obrnuto*plwidth,player.y-things[1].get_height(),plwidth,things[1].get_height()))
    playerportrait.draw_hearts(player.maxhealth,player.health)
    playerportrait.draw_stamina(player.maxstamina,player.stamina)
    pygame.display.update()
    lastframekeys=keys
    clock.tick(45)