from scipy import interpolate
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time  # to be used in timer
import pygame
import numpy as np
import random
from random import randint
pygame.init()


# Possible levels ==> [Score to pass, maximum time]
levels = [[40,30],[60,40],[80,50],[90,60],[100,70]]   # 5 levels
level = 1  # initial level


seconds = 0   # the actual timer of every level
time_start = 0  # just for calculating tome
######## Control the Small Fishes Motion ###########

x_ax = 50        #'INCREASING'  = increasing number of curve points which means'MORE' curve resolution(integer)
patterns_num=5   # Number of Available patterns (integer)

vertical_displacement = 5    #'DECREASING'  = decreasing vertical motion which means 'MORE STABLE' Motion
x_displacement = 0.2            # انا معملتش في دا حاجه دي سرعة x في السطر 239 جبتها هنا :D
##################################################


score=0
big_fish_size=2.2
texture=()
mouse_dir=1
photos=['Fishleft1.png','Fishright1.png','Fishleft2.png','Fishright2.png','Fishleft3.png','Fishright3.png','Fishleft4.png','Fishright4.png','Fishleft5.png','Fishright5.png','Fishleft6.png','Fishright6.png','Fishleft7.png','Fishright7.png','Fishleft8.png','Fishright8.png','Fishleft9.png','Fishright9.png','Fishleft10.png','Fishright10.png','Fishleft11.png','Fishright11.png','background.jpg','menu.png']


current_x = 200
current_y = 200




#Small Function to generate the vertical offset
def random_offset():
    return randint(vertical_displacement+10,600-vertical_displacement-10)




x_points = [i for i in range(-50,750,x_ax)]
num_points = len(x_points)

#A[0_X_pos, 1_Y_pos, 2_Scale, 3_dir_X, 4_pattern_num, 5_y_offset, 6 Shape ]

#The 7th dimension refers to the vertical offset
A =      [[0, 120 , 1.5, 1, 0, random_offset(), 1],
         [0  , 240, 3  , 1, 1, random_offset(), 3],
         [0  , 360, 1.5, 1, 2, random_offset(), 5],
         [0  , 480, 3  , 1, 3, random_offset(), 7],
         [0  , 600, 1.5, 1, 4, random_offset(), 9],
         [600, 120, 3  , -1, 4, random_offset(), 0],
         [600, 240, 1.5, -1, 3, random_offset(), 2],
         [600, 360, 3  , -1, 2, random_offset(), 4],
         [600, 480, 1.5, -1, 1, random_offset(), 6],
         [600, 600, 3  , -1, 0, random_offset(), 8]]
count =len(A)

paths = []
lost_flag=0

def generate_patterns():
    global paths, num_points, patterns_num, vertical_displacement
    paths = [] # clear paths
    for j in range(patterns_num):
        new_path = []
        for i in range(num_points):
            new_path.append(randint(300-vertical_displacement , 300+vertical_displacement))

        paths.append(interpolate.splrep(x_points, new_path))   # tck


def f(i):
    global paths,A

    if A[i][3] == 1:
        f_x = interpolate.splev(A[i][0],paths[A[i][4]])
    else:
        f_x = 600 - interpolate.splev(A[i][0],paths[A[i][4]])

    if A[i][0] > 650:
        A[i][3] = -A[i][3]
        A[i][6]=A[i][6]-1 #look at

    elif A[i][0]< -50:
        A[i][3] = -A[i][3]
        A[i][6]=A[i][6]+1



    return f_x + A[i][5] - 300

def drawText(string, x, y):
    glLineWidth(5)
    glColor(1, 1, 0)  # Yellow Color
    glLoadIdentity()
    glTranslate(x, y, 0)
    glRotate(180,1,0,0)
    glScale(.26, .26, 1)
    string = string.encode()  # conversion from Unicode string to byte string
    for c in string:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, c)


def add_small_fish():
    global count,A
    count += 1

    new_rand_x = random.choice([-20, 620])

    new_rand_pattern = randint(0, patterns_num - 1)
    if score <= 30:
        scale = 1.5
    else:
        scale = random.choice([1.5, 3])
    if new_rand_x == 0:
        new_fish_shape=random.choice([1,3,5,7,9,11,13,15,17,19])
        direction = 1
    else:
        new_fish_shape = random.choice([0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
        direction = -1
    A.append(list((new_rand_x, 0, scale, direction, new_rand_pattern, random_offset(),new_fish_shape)))

def remove_small_fish(i):
    global A,count
    global A
    del A[i]
    count-=1

def remove_big_fish_lost():
    global lost_flag
    lost_flag=1


def increase_Score():
    global score
    score +=1

def eating_soound():
    s_file = pygame.mixer.Sound("eating.wav")
    s_file.play()

def game_over_sound():
    s_file = pygame.mixer.Sound("gameover.wav")
    s_file.play()



def collsion (i):
    global current_x,current_y,score,count,patterns_num,big_fish_size,seconds
    x=A[i][0]
    y=A[i][1]
    if abs(current_x -x) <30 and abs(current_y-y)<30 and A[i][2] > big_fish_size :

        remove_big_fish_lost()
        game_over_sound()


    elif abs(current_x -x) <30 and abs(current_y-y)<30 and A[i][2] < big_fish_size :
        remove_small_fish(i)
        increase_Score()
        add_small_fish()
        eating_soound()










def load_texture():
    global texture,photos
    texture=glGenTextures(24)
    for i in range(24):
        imgload = pygame.image.load(photos[i])
        img = pygame.image.tostring(imgload, "RGBA", 1)
        width = imgload.get_width()
        height = imgload.get_height()
        glBindTexture(GL_TEXTURE_2D, texture[i])  # Set this image in images array
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexImage2D(GL_TEXTURE_2D, 0, 4, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture[i])




def myint():

    s_file = pygame.mixer.Sound("feeding-frenzy.wav")
    s_file.play()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,600,600,0,0,600)
    load_texture()
    #gluLookAt(0,0,1,0,0,0,0,1,0) #eye, look at, up vector
    glClearColor(1,1,1,.5)
    generate_patterns()


def start_again():
    global lost_flag, A,score,big_fish_size,score,time_start

    A = [[0, 120 , 1.5, 1, 0, random_offset(), 1],
         [0  , 240, 3  , 1, 1, random_offset(), 3],
         [0  , 360, 1.5, 1, 2, random_offset(), 5],
         [0  , 480, 3  , 1, 3, random_offset(), 7],
         [0  , 600, 1.5, 1, 4, random_offset(), 9],
         [600, 120, 3  , -1, 4, random_offset(), 0],
         [600, 240, 1.5, -1, 3, random_offset(), 2],
         [600, 360, 3  , -1, 2, random_offset(), 4],
         [600, 480, 1.5, -1, 1, random_offset(), 6],
         [600, 600, 3  , -1, 0, random_offset(), 8]]
    score = 0
    big_fish_size = 2.2
    lost_flag = 0

    time_start = time.time()

def start_time():
    global time_start
    time_start = time.time()


###########################################################
def menu ():
    global texture
    glBindTexture(GL_TEXTURE_2D, texture[-1])
    glColor(1,1,1)
    glBegin(GL_QUADS)
    glTexCoord(1,1)
    glVertex3f(0,0, 0)
    glTexCoord(0,1)
    glVertex3f(600,0 , 0)
    glTexCoord(0,0)
    glVertex3f(600,600, 0)
    glTexCoord(1,0)
    glVertex3f(0,600, 0)
    glEnd()

    glFlush()


def keyboard(key,x,y):
    global level
    if key == b"x":
        sys.exit()
    if key == b"a": #play
        start_time()
        glutIdleFunc(main_scene)

    if key == b"r":#statr again
        start_again()
        glutIdleFunc(main_scene)




##########################################################################################



def main_scene ():
    global texture,current_x,current_y , current_z ,count,big_fish_size,A, lost_flag,mouse_dir,score,levels,level
    if lost_flag == 1:
        glutIdleFunc(menu)



    if score >=20 :
        big_fish_size= 5



    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT) #| GL_DEPTH_BUFFER_BIT)
    if lost_flag!=1: #plar the game


        glBindTexture(GL_TEXTURE_2D, texture[22]) #background

        glBegin(GL_QUADS)
        glTexCoord(0, 0)
        glVertex3f(600,600 , 0)
        glTexCoord(0, 1)
        glVertex3f(600,0 , 0)
        glTexCoord(1, 1)
        glVertex3f(0,0 , 0)
        glTexCoord(1, 0)
        glVertex3f(0,600, 0)
        glEnd()


 #Texture Added
        string = "Score:" + str(score)
        print(string)
        drawText(string, 20,40 )
        glLoadIdentity()

        #Texture Added
        string = "Timer:" + str(levels[level-1][1]-seconds)
        print(string)
        drawText(string, 20, 100)
        glLoadIdentity()

        #Texture Added
        string = "Level:" + str(level)
        print(string)
        drawText(string, 20, 70)
        glLoadIdentity()

        glTranslate(current_x, current_y,0)
        glColor4f(1, 1, 1, 1)
        if mouse_dir==1:
            glBindTexture(GL_TEXTURE_2D, texture[21])
        else:
            glBindTexture(GL_TEXTURE_2D, texture[20])

        glBegin(GL_QUADS)
        glTexCoord(0, 0)
        glVertex3f(-10 * big_fish_size, 10 * big_fish_size, 0)
        glTexCoord(0, 1)
        glVertex3f(-10 * big_fish_size, -10 * big_fish_size, 0)
        glTexCoord(1, 1)
        glVertex3f(10 * big_fish_size, -10 * big_fish_size, 0)
        glTexCoord(1, 0)
        glVertex3f(10 * big_fish_size, 10 * big_fish_size, 0)
        glEnd()
        glLoadIdentity()

    if lost_flag != 1:

        for i in range(count):
            glLoadIdentity()
            A[i][1]=f(i)
            glTranslate(A[i][0],A[i][1],0)

            A[i][0] += (A[i][3] * x_displacement)


            if A[i][3]==1:
                glBindTexture(GL_TEXTURE_2D, texture[A[i][6]])
            if A[i][3] == -1:
                glBindTexture(GL_TEXTURE_2D, texture[A[i][6]])



            glBegin(GL_QUADS)
            glTexCoord(0,0)
            glVertex3f(-10 *A[i][2], 10 *A[i][2], 0)
            glTexCoord(0,1)
            glVertex3f(-10*A[i][2], -10*A[i][2], 0)
            glTexCoord(1,1)
            glVertex3f(10 *A[i][2], -10 *A[i][2], 0)
            glTexCoord(1,0)
            glVertex3f(10*A[i][2], 10 *A[i][2], 0)
            glEnd()
            collsion(i)
            print("score= ",score,"  level = ",level,"seconds=",seconds)

    glFlush()

    ###################### Levels ###########################################
    # Check for the Level

    if score >= levels[level-1][0]:    # Only 5 levels then get Error
        next_level(level)
        glutIdleFunc(main_scene)


    # continue timer
    game_timer()


def game_timer():
    global seconds,time_start,levels,level, lost_flag


    seconds = int(time.time() - time_start)
    if seconds >= levels[level-1][1]:
        lost_flag = 1

def next_level(i):

    global x_displacement,patterns_num,vertical_displacement,level
    x_displacement += i * 0.2
    vertical_displacement += 20
    patterns_num += i*2
    generate_patterns()
    level += 1
    start_again()

def mouse(new_x, new_y):
    global current_x, current_y,mouse_dir
    if new_x >current_x :
        mouse_dir = 1
    else:
        mouse_dir = -1
    current_x = new_x
    current_y = new_y


def main():

    glutInit()                                  # Initialize Glut Features
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)    # Initialize Window Options
    glutInitWindowSize(600,600)
    glutCreateWindow(b"fish")
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)   # Blend
    glEnable(GL_BLEND)

    myint()
    glutKeyboardFunc(keyboard)
    glutIdleFunc(menu)
    glutPassiveMotionFunc(mouse)
    glutDisplayFunc(menu)
    glutMainLoop()

main()
