import pygame,sys,random
pygame.init();game_active=False;game_started=False

window=pygame.display.set_mode((960,640))
pygame.display.set_caption('kalahalla')
music=pygame.mixer.Sound('assets/sundrive.mp3')
music.play(loops=-1)

font=pygame.font.Font(None,50)
background=pygame.image.load('assets/background2.jpeg').convert()
menu=pygame.image.load('assets/menu.jpg').convert()
window.blit(menu,(160,0));pygame.display.update()
end=pygame.image.load('assets/die.png').convert()

platform=pygame.image.load('assets/platform2.png').convert()
platform_rect=platform.get_rect(topleft=(0,580))

spooderR=pygame.image.load('assets/spooderR.png').convert_alpha()
spooderL=pygame.image.load('assets/spooderL.png').convert_alpha()
spooder_moveL=pygame.image.load('assets/spooder_moveL.png').convert_alpha()
spooder_moveR=pygame.image.load('assets/spooder_moveR.png').convert_alpha()
spooder_move=[spooderL,spooderR,spooder_moveL,spooder_moveR]
spooder_index=1

spooder_rect=spooder_move[spooder_index].get_rect(midbottom=(0,590))
health=100;death=pygame.mixer.Sound('assets/roblox-death-sound-effect.mp3')
velocity_player=15
score=0

nuke=pygame.image.load('assets/nuke2.png').convert_alpha()
nuke_timer=pygame.USEREVENT+1
pygame.time.set_timer(nuke_timer,500)
velocity_nuke=5
g=0.2;explosion=pygame.mixer.Sound('assets/explosion.wav')

nuke_list=[]
def nuke_fall(nuke_list):
    global health
    if nuke_list:
        for nuke_parameters in nuke_list:
            nuke_parameters[0].y+= nuke_parameters[1]
            nuke_parameters[1]+=g
            if nuke_parameters[0].colliderect(spooder_rect) and not(nuke_parameters[2]):health-=20;nuke_parameters[2]=True;explosion.play()
            window.blit(nuke,nuke_parameters[0])
        nuke_list=[nuke_parameters for nuke_parameters in nuke_list if nuke_parameters[0].y<550]

        return nuke_list
    else:return []

clock=pygame.time.Clock()

def disp_score(score):
    score_surf=font.render('score:'+str(score),False,'pink')
    score_rect=score_surf.get_rect(center=(480,30))
    window.blit(score_surf,score_rect)

def disp_health():
    health_surf=font.render('health:'+str(health),False,'red')
    health_rect=health_surf.get_rect(center=(100,30))
    window.blit(health_surf,health_rect)


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit();sys.exit()
        elif event.type==pygame.KEYUP and not(game_active):
            pygame.time.delay(500)
            game_active=True
            health=100;score=0

        elif event.type==nuke_timer and game_active:
            nuke_list.append([nuke.get_rect(topleft=(random.randint(0,960),0)),velocity_nuke,False])
            score+=10

    if game_active:
        game_started=True
        window.blit(background,(0,0))
        window.blit(platform,platform_rect)

# hand part
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spooder_rect.left-=velocity_player;spooder_index=2
            window.blit(spooder_moveL,spooder_rect)
        elif keys[pygame.K_RIGHT]:
            spooder_rect.left+=velocity_player;spooder_index=3
            window.blit(spooder_moveR,spooder_rect)
        else:
            if spooder_index in (2,0):spooder_index=0;window.blit(spooderL,spooder_rect)
            elif spooder_index in (1,3):spooder_index=1;window.blit(spooderR,spooder_rect)
# hand part end

        if spooder_rect.left>960:spooder_rect.right=0
        elif spooder_rect.right<0:spooder_rect.left=960
        
        nuke_list=nuke_fall(nuke_list)
        disp_health();disp_score(score)
        if health==0:game_active=False;death.play()
    
    elif not(game_active) and game_started:
            window.fill('black')
            window.blit(end,(154.5,83.5))
            disp_score(score)
    pygame.display.update()
    clock.tick(70)