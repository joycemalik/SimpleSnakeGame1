import pygame
import random
import os


#colour
white=(255,255,255)
red=(234,80,88)
black=(1,1,1)

#display
screen_height=720
screen_width=1200
x=pygame.init()
gameWindow=pygame.display.set_mode((screen_width,screen_height))
pygame.mixer.init()
pygame.display.set_caption("Snake vs Mr JOYSiM")
clock=pygame.time.Clock()

#font
font=pygame.font.SysFont(None,55)
font_path = "hyperwave-one.ttf"
font_size = 60
futuristic_font = pygame.font.Font(font_path, font_size)

# Create text surface
bgimg=pygame.image.load("bg.png")
overimg=pygame.image.load("over.png")
wlcimg=pygame.image.load("wlc.png")
bgimg=pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()
wlcimg=pygame.transform.scale(wlcimg,(screen_width,screen_height)).convert_alpha()
overimg=pygame.transform.scale(overimg,(screen_width,screen_height)).convert_alpha()

# sfx
hover_sound = pygame.mixer.Sound("hover.mp3")
sound_played=False

def startMusic():
    button_click_sound = pygame.mixer.Sound("start.mp3")   
    button_click_sound.play() 
    pygame.mixer.music.load("bg.mp3")
    pygame.time.delay(950)
    pygame.mixer.music.play(-1)

def checkStart(mouse_x,mouse_y):
    if 638 < mouse_x < 1097 and 260 < mouse_y < 392:    
        startMusic()                
        gameloop()

def welcomeFor():
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            button_click_sound = pygame.mixer.Sound("start.mp3")   
            button_click_sound.play()
            return True
        
        

        if event.type==pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            checkStart(mouse_x,mouse_y)
        
        if event.type==pygame.KEYDOWN and event.key==pygame.K_SPACE:
            startMusic()
            gameloop()

def text_screen(text,color,x,y):
    screen_text=font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y])

def plot_snake(gameWindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.circle(gameWindow,color,[x,y],snake_size-5)

def welcome():
    exit_game=False
    while not exit_game:
        gameWindow.blit(wlcimg,(0,0))
        exit_game=welcomeFor()
        pygame.display.update()
        clock.tick(60)
    button_click_sound = pygame.mixer.Sound("start.mp3")   
    button_click_sound.play()
    pygame.time.delay(750)
    pygame.quit()
    exit()
        
# gameWindow.fill((196,170,229))
# text_screen("Welcome to Snake Game",black,screen_width/3.5,screen_height/2)
# text_screen("Press Spacebar to Play",black,screen_width/3.45,screen_height/1.8)

def displayScore(score):
    Score_font=pygame.font.Font(font_path, 100)
    Score_end = Score_font.render(str(score), True, white)
    Score_end_pos=(605,480)
    gameWindow.blit(Score_end,Score_end_pos)

def resetMusic():
    pygame.mixer.music.load("reset.mp3")
    pygame.mixer.music.play()
    welcome()

def resetFor():
    
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            return True
        # if event.type == pygame.MOUSEMOTION:
        #     mouse_x, mouse_y = event.pos
        #     if checkMClickButton((mouse_x, mouse_y),(488,583),(710,658)) and not sound_played:
        #         hover_sound.play()
        #         sound_played=True
        #     elif not sound_played:
        #         sound_played=False
        if event.type==pygame.MOUSEBUTTONDOWN :
            if checkMClickButton(pygame.mouse.get_pos(),(488,583),(710,658)):
                resetMusic()
        if event.type==pygame.KEYDOWN and event.key==pygame.K_RETURN:
            resetMusic()

def checkMClickButton(act_pos:tuple,min:tuple,max:tuple):
    try:
        x,y=act_pos
        x1,y1=min
        x2,y2=max
        return x1 < x < x2 and y1 < y < y2
    except Exception as e:
        print(e)
        return False

def gameInputs(velocity_x,velocity_y,top_v):
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            return [True,velocity_x,velocity_y,top_v]

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT and velocity_x != -top_v :
                velocity_x=top_v
                velocity_y=0
            if event.key==pygame.K_LEFT and velocity_x != top_v:
                velocity_x=-top_v
                velocity_y=0
            if event.key==pygame.K_UP and velocity_y != top_v:
                velocity_x=0
                velocity_y=-top_v
            if event.key==pygame.K_DOWN and velocity_y != -top_v:
                velocity_x=0
                velocity_y=top_v
            if event.key==pygame.K_ESCAPE:
                velocity_x=0
                velocity_y=0
                # is_paused=True
    return [False,velocity_x,velocity_y,top_v]

def boundaryCondition(x,y):
    if x<0 or x>screen_width or y<0 or y>screen_height:
        pygame.mixer.music.load("gover.mp3")
        pygame.mixer.music.play()
        return True
    return False

# game loop
def gameloop():
    
    fps=90
    score=0
    exit_game=False
    game_over=False
    is_paused=False
    snake_x=screen_width/2
    snake_y=screen_height/2
    snake_size=17
    snk_length=1
    snk_list=[]
    velocity_x=0
    velocity_y=0
    top_v=1
    food_x=random.randint(screen_width//10,(3*screen_width)//4)
    food_y=random.randint(screen_height//10,(3*screen_height)//4)
    eat= pygame.mixer.Sound("eat.mp3") 
    # check if score file exists...
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f:
            highscore=f.write("0")     
    with open("highscore.txt","r") as f:
        highscore=f.read()

    while(exit_game!=True and not is_paused):
        if game_over:
            with open("highscore.txt","w") as f:
                f.write(str(highscore))
            gameWindow.blit(overimg,(0,0))
            displayScore(score)
            exit_game=resetFor()
            


        else:
            
            exit_game,velocity_x,velocity_y,top_v=gameInputs(velocity_x,velocity_y,top_v)
            
            snake_x +=velocity_x
            snake_y +=velocity_y

            game_over=boundaryCondition(snake_x,snake_y)

           
            if(abs(snake_x-food_x)<15 and abs(snake_y-food_y)<15 ):
                score+=10
                
                food_x=random.randint(screen_width//10,screen_width//2)
                food_y=random.randint(screen_height//10,screen_height//2)
                snk_length+=7.5
                top_v+=0.1
                if score>int(highscore):
                    highscore=score
                eat.play()
                pygame.mixer.music.unpause()


            head=[]
            head.append(snake_x)
            head.append(snake_y)    
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                pygame.mixer.music.load("gover.mp3")
                pygame.mixer.music.play()
                game_over=True

            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0,0))
            pygame.draw.circle(gameWindow,red,[food_x,food_y],snake_size-5)
            plot_snake(gameWindow,black,snk_list,snake_size)
            Score_disp = futuristic_font.render(f"Score: {score}                 High Score: {highscore}", True, red)
            gameWindow.blit(Score_disp, (5,5)) 
            # text_screen(f"Score: {score}                 High Score: {highscore}",red,5,5)
        pygame.display.update()
        clock.tick(fps)


    button_click_sound = pygame.mixer.Sound("start.mp3")   
    button_click_sound.play()
    pygame.time.delay(500)
    pygame.quit()
    exit()

welcome()