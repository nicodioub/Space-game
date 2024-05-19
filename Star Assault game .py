import pygame 
import os  #operating systems 
pygame.font.init()
pygame.mixer.init()

RED = (255,0,0)
YELLOW = (255,255,0)
LONGUEUR, LARGEUR = 900, 500
GREEN = (0, 255, 0)
BLACK = (0,0,0)
WHITE = (255, 255, 255)
BORDER = pygame.Rect(LONGUEUR//2 - 5,0,10,LARGEUR)
vel = 5
BULLET_VEL = 14
MAX_BULLETS = 3
FPS = 60 # frame per second 

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets_Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets_Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55 , 40

YELLOW_HIT = pygame.USEREVENT + 1 
RED_HIT = pygame.USEREVENT +2 

WINDOW = pygame.display.set_mode((LONGUEUR, LARGEUR))
pygame.display.set_caption("First game ")

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),-90)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('space.png')),(LONGUEUR,LARGEUR))


def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health): 
    pygame.draw.rect(WINDOW,BLACK,BORDER)
    WINDOW.blit(SPACE,(0,0))
    
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health),1 , WHITE )
    yellow_health_text = HEALTH_FONT.render('Health: ' + str(yellow_health), 1 , WHITE )
    WINDOW.blit(red_health_text,(LONGUEUR - red_health_text.get_width()- 10 , 10 ))
    WINDOW.blit(yellow_health_text, (10,10))

    WINDOW.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WINDOW.blit(RED_SPACESHIP,(red.x,red.y))



    for bullet in red_bullets:
          pygame.draw.rect(WINDOW,RED,bullet)

    for bullet in yellow_bullets:
          pygame.draw.rect(WINDOW,YELLOW,bullet)

    pygame.display.update()

def yellow_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_q] and yellow.x - vel > 0: #left
            yellow.x -= vel  
    if keys_pressed[pygame.K_d] and yellow.x + vel + yellow.width < BORDER.x : # right 
            yellow.x += vel 
    if keys_pressed[pygame.K_z] and yellow.y - vel > 0 : #up
            yellow.y -= vel         
    if keys_pressed[pygame.K_s] and yellow.y + vel + yellow.height < LARGEUR - 15: #down 
            yellow.y += vel 

def red_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x - vel  > BORDER.x + BORDER.width : #left
            red.x -= vel  
    if keys_pressed[pygame.K_RIGHT] and red.x + vel + red.width < LONGUEUR: # right 
            red.x += vel 
    if keys_pressed[pygame.K_UP] and red.y - vel  > 0: #up
            red.y -= vel 
    if keys_pressed[pygame.K_DOWN] and red.y + vel +red.height < LARGEUR - 15 : #down 
            red.y += vel 


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets : 
            bullet.x += BULLET_VEL
            if red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                yellow_bullets.remove(bullet)
            elif bullet.x > LONGUEUR :
                  yellow_bullets.remove(bullet)

    for bullet in red_bullets : 
            bullet.x -= BULLET_VEL
            if yellow.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                red_bullets.remove(bullet)
            elif bullet.x < 0 :
                  red_bullets.remove(bullet)
def draw_winner(text): 
      draw_text = WINNER_FONT.render(text,1 ,WHITE )
      WINDOW.blit(draw_text,(LONGUEUR // 2 - draw_text.get_width()//2, LARGEUR//2 - draw_text.get_height()//2 ))
      pygame.display.update()
      pygame.time.delay(5000)




def main(): 
    red = pygame.Rect(750,200,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect(150,200,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red_bullets = []
    red_health = 10
    yellow_health = 10 
    yellow_bullets = []


    clock = pygame.time.Clock()
    run = True 
    while run : 
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False 
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                      bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2,10,5)
                      yellow_bullets.append(bullet)
                      BULLET_FIRE_SOUND.play()
                        
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x , red.y + red.height//2 - 2,10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT :
                  red_health -= 1
                  BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT :
                  yellow_health -= 1 
                  BULLET_HIT_SOUND.play()

        winner_text = ''
        if red_health <= 0 :
            winner_text = "Yellow Wins ! "
        if yellow_health <= 0 :
            winner_text = 'Red Wins ! '     

        if winner_text  != "":
              draw_winner(winner_text)
              break

        print(red_bullets,yellow_bullets)
        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed,yellow)
        red_movement(keys_pressed,red)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)


        draw_window(red,yellow,red_bullets,yellow_bullets, red_health, yellow_health )

    #pygame.quit() #Quitter apres victoire 
    main() #Relancer apres victoire



if __name__ == '__main__':
    main()
