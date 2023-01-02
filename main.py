import pygame
from tkinter import *
from tkinter import messagebox
from sys import exit
import random

screen_size = [448, 600]
screen = pygame.display.set_mode(screen_size)
pygame.font.init()
pygame_icon = pygame.image.load('logo.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Money Rain")
level = 3
fram_num = 0
user_face = 1
heart_num = 3
when_crash = 1
when_crash2 = 1

money = pygame.image.load('money.png')
user1 = pygame.image.load('user1.png')
user2 = pygame.image.load('user2.png')
user3 = pygame.image.load('user3.png')
police = pygame.image.load('police.png')
heart = pygame.image.load('heart.png')
label = pygame.image.load('label.png')

def display_score(score):
    x = -157
    if (score >= 10) and (score < 100) and (score >= 0):
        x = -140    
    elif (score >= 100) and (score < 1000):
        x = -122
    elif(score >= 1000):
        x = -104
    elif (score <= -10) and (score > -100):
        x = -130    
    elif (score <= -100) and (score > -1000):
        x = -112
    screen.blit(label, [x ,-43])
    font = pygame.font.SysFont('Comic Sans MS', 30)
    score_text = 'Money: ' + str(score) + '$'  
    color = '#ffffff' 
    text = font.render(score_text, True, color)
    screen.blit(text, [9, 0])

def random_offset():
    return -1 * random.randint(100, 1500)

def police_random_offset():
    return (-1 * random.randint(600, 4000)) - 150

money_y = [random_offset(), random_offset(), random_offset(), random_offset()]
police_y = [police_random_offset(), police_random_offset(), police_random_offset(), police_random_offset()]
user_x = 180
score = 0


def crashed(idx):
    global score
    global keep_alive
    score  = score + 10
    money_y[idx] = random_offset()

def police_crashed(idx):
    global score
    global heart_num
    global when_crash
    global when_crash2
    if when_crash == 1:
        when_crash = score
    else:
        when_crash2 = score

    score  = score - 10    
    print("Crashed with police", idx+1, score)
    
    heart_num = heart_num - 1

    police_y[idx] = police_random_offset()

def increase_heart(heart_num):
    global when_crash
    global when_crash2
    global score
    if (score - when_crash == 500) or (score - when_crash2 == 500):
        if heart_num == 3:
            return 0 
        elif heart_num == 2:
            when_crash = 1
            return 1
        elif heart_num == 1:
            when_crash = 1
            return 1
    else:
        return 0

def update_money_pos(idx, level):
    global score
    
    if money_y[idx] > 600:
        money_y[idx] = random_offset()
    else:
        money_y[idx] = money_y[idx] + level 

def update_police_pos(idx, level):
    global score
    if police_y[idx] > 600:
        police_y[idx] = police_random_offset()
    else:
        police_y[idx] = police_y[idx] + level

def level_num(score):
    if score >= 150 and score < 300:
        return 4
    elif score >= 300 and score < 500:
        return 5
    elif score >= 500:
        return 6
    else:
        return 3

keep_alive = True
clock = pygame.time.Clock()

def game_over():
    global keep_alive   
    global heart_num   
    global score
    global level
    messagebox.showinfo(title="Oops :(", message="GAME OVER!")
    answer = messagebox.askyesno(title="Yes or No", message="Do you want to play again?")
    if answer == True:
        heart_num = 3
        score = 0
        level = 3
        return True
    elif answer == False:
       print("Have a nice day!")
       return False

def play_game(keep_alive):
    global fram_num
    global user_x
    global heart_num

    while keep_alive:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and user_x < 343:
            user_x = user_x + 10
        elif (keys[pygame.K_LEFT] or keys[pygame.K_a]) and user_x > 43:
            user_x = user_x - 10
        if keys[pygame.K_ESCAPE]:
            keep_alive = False 
        if keys[pygame.K_p]:
            p_answer = messagebox.askyesno(title="Paused", message="Do you want to continue?")
            if p_answer == True:
                pass
            elif p_answer == False:
                keep_alive = False
        
        level = level_num(score)    

        update_money_pos(0, level)
        update_money_pos(1, level)
        update_money_pos(2, level)
        update_money_pos(3, level)

        update_police_pos(0, level)
        update_police_pos(1, level)
        update_police_pos(2, level)
        update_police_pos(3, level)
        
        
        fram_num = fram_num + 1
        if (fram_num == 280):
            fram_num = 281

        if fram_num == 391 :
            fram_num = 2

        fram_name = str(fram_num)+ '.jpg'
        full_name = 'final_road\\' + fram_name
        background = pygame.image.load(full_name)
        screen.blit(background, [0,0])
    
        if heart_num == 3:
            screen.blit(user1, [user_x, 535])
        elif heart_num == 2:
            screen.blit(user2, [user_x, 535])
        elif heart_num == 1:
            screen.blit(user3, [user_x, 535]) 
        else:
            keep_alive = game_over()

        screen.blit(money, [45, money_y[0]])
        screen.blit(money, [137, money_y[1]])
        screen.blit(money, [230, money_y[2]])
        screen.blit(money, [325, money_y[3]])
        
        screen.blit(police, [45, police_y[0]])
        screen.blit(police, [137, police_y[1]])
        screen.blit(police, [230, police_y[2]])
        screen.blit(police, [325, police_y[3]])

        if heart_num == 3:
            screen.blit(heart, [375, -17])
            screen.blit(heart, [326, -17])
            screen.blit(heart, [276, -17])
        if heart_num == 2:
            screen.blit(heart, [326, -17])
            screen.blit(heart, [375, -17])
        if heart_num == 1:
            screen.blit(heart, [375, -17])

        if money_y[0] > 485 and user_x < 97:
            crashed(0)

        if money_y[1] > 485 and user_x > 80 and user_x < 200:  
            crashed(1)

        if money_y[2] > 485 and user_x > 190 and user_x < 290:
            crashed(2)

        if money_y[3] > 485 and user_x > 280 and user_x < 343:
            crashed(3)

        
        if police_y[0] > 452 and police_y[0]< 560 and user_x < 97:
            police_crashed(0)

        if police_y[1] > 452 and police_y[1]< 560 and user_x > 80 and user_x < 200:  
            police_crashed(1)

        if police_y[2] > 452 and police_y[2]< 560 and user_x > 190 and user_x < 290:
            police_crashed(2)

        if police_y[3] > 452 and police_y[3]< 560 and user_x > 280:
            police_crashed(3)

        heart_num = heart_num + increase_heart(heart_num)

        display_score(score)
        pygame.display.update()
        clock.tick(60)

if keep_alive == True: 
    play_game(keep_alive)
