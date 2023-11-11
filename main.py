import pygame,sys,random

#to start the game
pygame.init()
game_active=False   #to check if the game if the running
game_started=False  #to check if the game started

#to create a window
window=pygame.display.set_mode((960,640))
pygame.display.set_caption('spooder game')

#game start screen
start_screen=pygame.image.load('assets/start_screen.jpg').convert()
window.blit(start_screen,(160,0))
pygame.display.update()

#game background and background music
background=pygame.image.load('assets/background2.jpeg').convert()
music=pygame.mixer.Sound('assets/sundrive.mp3')
music.play(loops=-1)

#sound effects
death=pygame.mixer.Sound('assets/roblox-death-sound-effect.mp3')
explosion=pygame.mixer.Sound('assets/explosion.wav')

#platform rect
platform=pygame.image.load('assets/platform2.png').convert()
platform_rect=platform.get_rect(topleft=(0,580))

#player frames
spooderR=pygame.image.load('assets/spooderR.png').convert_alpha()
spooderL=pygame.image.load('assets/spooderL.png').convert_alpha()
spooder_moveL=pygame.image.load('assets/spooder_moveL.png').convert_alpha()
spooder_moveR=pygame.image.load('assets/spooder_moveR.png').convert_alpha()
spooder_move=[spooderL,spooderR,spooder_moveL,spooder_moveR]
spooder_index=1

#player rect and attributes
spooder_rect=spooder_move[spooder_index].get_rect(midbottom=(0,590))
health=100
velocity_player=15
score=0

#nuke rect and attributes
nuke=pygame.image.load('assets/nuke2.png').convert_alpha()
velocity_nuke=5
g=0.2
nuke_list=[]
explosion_cloud=pygame.image.load('assets/explosion.png')

#timer which activates every 0.7 seconds to spawn a nuke
nuke_timer=pygame.USEREVENT+1
pygame.time.set_timer(nuke_timer,700)

#manages nuke list, collisions and nuke spawn
def nuke_fall(nuke_list):
    global health
    if nuke_list:
        #nuke parameters contains [nuke rect , velocity , collision checker(T/F)]
        for nuke_parameters in nuke_list:
            #moves the nuke
            nuke_parameters[0].y+= nuke_parameters[1]
            nuke_parameters[1]+=g
            #collisions
            collided=nuke_parameters[2]
            if nuke_parameters[0].colliderect(spooder_rect) and not(collided):
                health-=20
                nuke_parameters[2]=True
                explosion.play()
                window.blit(explosion_cloud,nuke_parameters[0].topleft)
            window.blit(nuke,nuke_parameters[0])
        #removes exploded nukes and nukes that missed from the nuke list
        nuke_list=[nuke_parameters for nuke_parameters in nuke_list if nuke_parameters[0].y<550 and not(nuke_parameters[2])]

        return nuke_list
    else:return []

#game fps controller
clock=pygame.time.Clock()

#score count and health
font=pygame.font.Font(None,50)
def disp_score(score):
    score_surf=font.render('score:'+str(score),False,'pink')
    score_rect=score_surf.get_rect(center=(480,30))
    window.blit(score_surf,score_rect)

def disp_health():
    health_surf=font.render('health:'+str(health),False,'red')
    health_rect=health_surf.get_rect(center=(100,30))
    window.blit(health_surf,health_rect)

#game end screen
end=pygame.image.load('assets/die.png').convert()

#game loop
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: #to quit the game
            pygame.quit()
            sys.exit()

        elif event.type==pygame.KEYUP and not(game_active): #to start/restart the game
            pygame.time.delay(500)
            game_active=True
            health=100
            score=0

        elif event.type==nuke_timer and game_active:    #to periodically spawn nukes
            #whenever the timer returns True, a nuke is added to the nuke list
            nuke_list.append(
                [nuke.get_rect(topleft=(random.randint(0,960),0)),velocity_nuke,False]
                )
            score+=10

    if game_active: #the actual game part
        game_started=True
        window.blit(background,(0,0))
        window.blit(platform,platform_rect)
        
        #to get what key the player pressed
        #it is a dictionary like object with bool values
        keys=pygame.key.get_pressed()

        #to move the player
        if keys[pygame.K_LEFT]:
            spooder_rect.left-=velocity_player
            spooder_index=2
            window.blit(spooder_moveL,spooder_rect)
        
        elif keys[pygame.K_RIGHT]:
            spooder_rect.left+=velocity_player
            spooder_index=3
            window.blit(spooder_moveR,spooder_rect)
        
        #player idle position
        else:
            if spooder_index in (2,0):
                spooder_index=0
                window.blit(spooderL,spooder_rect)
            
            elif spooder_index in (1,3):
                spooder_index=1
                window.blit(spooderR,spooder_rect)

        #to stop the player from exiting the screen
        if spooder_rect.left>960:
            spooder_rect.right=0
        
        elif spooder_rect.right<0:
            spooder_rect.left=960
        
        #to update nuke_list, health and score
        nuke_list=nuke_fall(nuke_list)
        disp_health()
        disp_score(score)
        
        #to check if player is dead
        if health==0:
            game_active=False
            death.play()
    
    #game ending screen
    elif not(game_active) and game_started:
            window.fill('black')
            window.blit(end,(154.5,83.5))
            disp_score(score)
    
    #to update the screen every frame and to control frame rate
    pygame.display.update()
    clock.tick(70)