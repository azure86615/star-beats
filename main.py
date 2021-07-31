import numpy as np
import pygame, sys, random, time
from pygame.locals import *

#設置遊戲視窗
display_width = 1080
display_height = 920

windowSurface = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Star Beats')


#變數宣告
BACKGROUNDCOLOR = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PURPLE = (155, 55, 185)
PINK = (255, 0, 255)
HpFrame = (153, 217, 234)
FPS = 180

Game_start = False      #判斷是否為開始畫面
global Hit              #各個參數紀錄
Hit = 0
global Miss
Miss = 0
global Combo
Combo = 0
global HighC
HighC = 0

Speed = 10
#各道的拍點時機 (單位:格)
path1 = [21.5,29.5,48,53,66,70,72,73.5,86,90,98,107,118,124,132,140,148,156,172,184,186,188,191,198,207,211,214,224,235,240,244,245.5,304,320,328,336,340,342,351,353,359,367,374,395.5,398,408,410,422,425.5,428,446,461,471,475,478,482,488,490,512]
path2 = [20,32,39,44,56,58,64,77.5,83,85,88,96,99,104,108,110,114,120,128,138,144,152,157,160,165,176,182,192,193,195,203,205,206,222,231,257,258,259,262,267,268,272.5,273.5,278.5,283,284,288.5,289.5,299,302,312,325.5,330,333,344,354,357,363,365,369,379,384,390,392,394,400,405,420,427,431,434,436,439,442,449,457,459,463]
path3 = [16,36,54.5,60,62,69,75,80,81.5,92,94,105.5,116,122,136,142,154,170,179,189.5,200,201,208,209,216,217,219,221,226,228,233,237.5,247,256,260,261,264,265,270,271,275.5,276.5,280,281,286,287,291.5,292.5,293.5,296,303,310,311,313.5,316,318,321.5,345,349,355.5,361,371.5,373,376,380,383,385.5,403,411,414,418,424,438,445,450,453,455,458,460,467,485,491]
path4 = [15,132,148,162,164,323,327,342,347,374,408,410,416,422,428,443]
path5 = [28,31,67,73.5,76,77.5,86,91,100,102,105.5,108,110,128,139,144,158,168,178,183,189.5,194,199,205,215,225,229.5,234,252,254,257.5,258.5,259.5,267.5,268.5,272,273,278,279,283.5,284.5,288,289,302,313.5,319,325.5,346,355,358,366,370,387,393,395,398,406,420,430,437,451,457,459,471,479,481]
path6 = [15.5,23,32,37.5,54,55,58,60,71,81.5,89,97,104,107,141,155,161,181,188,210,218,221,239,244,245.5,256,260.5,261.5,264.5,265.5,270.5,275,276,280.5,281.5,286.5,291,292,293,310.5,315,321.5,329,334,347.5,350,362,371,377.5,380,382,388,390,401.5,411,414,418,424,431,434,436,439,447,449,458,460,465,477,486]
path7 = [18,52,62,64,68,79,112,124,137,153,166,176,180,184,186,191,196,197,202,212,213,227,232,236,247,250,294,296,305.5,307,316,324,332,336,340,344,353,376,382,384,392,416,443,455,461,475,483,488,490,512]

#前處理
pathwidth = (display_width * 2 / 3) / 7         #軌道寬度
path = [path1, path2, path3, path4, path5, path6, path7]
maxclick = max(len(path1),len(path2),len(path3),len(path4),len(path5),len(path6),len(path7))
clickflag = [[0]*len(path1),[0]*len(path2),[0]*len(path3),[0]*len(path4),[0]*len(path5),[0]*len(path6),[0]*len(path7)]      #拍點性質，0為尚未判定過，1為以判定(沒被打到)，2為有打到的判定
for i in range(len(path)):
    for j in range(len(path[i])):
        path[i][j] *= -0.215 * 950              #第一乘數功能:把[格]單位換成[秒]，第二乘數:控制拍點與拍點之間的間隔寬度
        path[i][j] += 2900                      #起始點 (應先控制此數字，

for j in range(len(path)):                      #path list的冗餘擴充，成二維方陣
    for i in range(maxclick - len(path[j])):
        path[j].append(5000)
        clickflag[j].append(1)                  #click flag的冗餘擴充，成二位陣列


#退出
def terminate():
	pygame.quit()
	sys.exit()


#打擊判定
def click(path_num):
    path_num = path_num - 1
    line_pos = display_height * 4 / 5
    #path[j][i]
    for i in range(len(path[path_num])):
        if path[path_num][i] - line_pos <= 80 and path[path_num][i] - line_pos >= -80 and clickflag[path_num][i] == 0:
            global Hit,Combo,HighC
            Hit += 1
            Combo += 1
            clickflag[path_num][i] = 2
            HighC = max(Combo,HighC)


#初始化
pygame.init()
mainClock = pygame.time.Clock()

#加載圖片
startImage = pygame.image.load('start.jpg')         #開始畫面
clickImage = pygame.image.load('yellowstar.png')          #拍點圖
lineImage = pygame.image.load('bar.png')           #打擊線圖
kakeraImage = pygame.image.load('kakera.png')       #打擊成功圖

click_width = 100
click_height = 60
clickImage = pygame.transform.scale(clickImage, (click_width, click_height))        #拍點圖，大小設置
kakera_width = 100
kakera_height = 60
kakeraImage = pygame.transform.scale(kakeraImage, (kakera_width, kakera_height))    #(有打到的)拍點圖，大小設置
line_width = 115
line_height = 80
lineImage = pygame.transform.scale(lineImage, (line_width, line_height))            #打擊線圖，大小設置

#加載音樂
music = pygame.mixer.Sound('Shin_Ai.wav')

#開始畫面
def startscreen():
    windowSurface.blit(startImage,(0,0))        #背景

    startText = pygame.font.Font('LucidaBrightDemiBold.ttf', 40)
    TextSurf = startText.render('Press Enter', True, WHITE)
    TextRect = TextSurf.get_rect()
    TextRect.center = (display_width /2, display_height /5 * 4)
    windowSurface.blit(TextSurf, TextRect)

    startText = pygame.font.Font('LucidaBrightDemiBold.ttf', 100)
    TextSurf = startText.render('Star Beats', True, YELLOW)
    TextRect = TextSurf.get_rect()
    TextRect.center = (display_width / 2, display_height / 2)
    windowSurface.blit(TextSurf, TextRect)
    pygame.display.update()

#遊戲畫面
def playscreen():
    music.play()                #開始播放音樂
    windowSurface.fill(BLACK)   #背景，黑色覆蓋
    for i in range(1,8,1):
        pygame.draw.line(windowSurface, WHITE, (pathwidth*i,0),(pathwidth*i,display_width))     #軌道分隔線

    startText = pygame.font.Font('LucidaBrightDemiBold.ttf', 50)
    s = 'Hit: ' + str(Hit)
    TextSurf = startText.render(s, True, PURPLE)
    TextRect = TextSurf.get_rect()
    TextRect.center = (display_width / 5 * 4, display_height / 4)
    windowSurface.blit(TextSurf, TextRect)

    s = 'Miss: ' + str(Miss)
    TextSurf = startText.render(s, True, WHITE)
    TextRect.center = (display_width / 5 * 4, display_height / 3)
    windowSurface.blit(TextSurf, TextRect)

    s = str(Combo) + '  Combos'
    TextSurf = startText.render(s, True, YELLOW)
    TextRect = TextSurf.get_rect()
    TextRect.center = (display_width / 6 * 5, display_height / 2)
    windowSurface.blit(TextSurf, TextRect)

    s = str(HighC) + '  HighCom'
    TextSurf = startText.render(s, True, PINK)
    TextRect = TextSurf.get_rect()
    TextRect.center = (display_width / 6 * 5, display_height / 3 * 2)
    windowSurface.blit(TextSurf, TextRect)

    for i in range(0,7):
        windowSurface.blit(lineImage, (i*pathwidth -5, display_height*4/5))



#遊戲主程式

while True:
    for event in pygame.event.get():
        #print(event)
        if event.type == QUIT:
            terminate()
        if event.type == KEYDOWN and event.key == 13:       #按下enter，進入遊戲
            firsttime = time.clock()
            Game_start = True

        if event.type == KEYDOWN:                           #打點按鍵，傳送道數的參數
            if event.unicode == 'z':
                click(1)
            if event.unicode == 'x':
                click(2)
            if event.unicode == 'c':
                click(3)
            if event.unicode == 'v':
                click(4)
            if event.unicode == 'b':
                click(5)
            if event.unicode == 'n':
                click(6)
            if event.unicode == 'm':
                click(7)


    if Game_start == False:
        startscreen()
    else:
        playscreen()
        for i in range(maxclick):
            for j in range(len(path)):
                path[j][i] += Speed
                if path[j][i] >= -60 and path[j][i] <= display_height:              #該拍點有在螢幕範圍內才畫出來
                    if clickflag[j][i] == 0 or clickflag[j][i] == 1:
                        windowSurface.blit(clickImage, (j*pathwidth, path[j][i]))   #未判定過的圖
                    else:
                        windowSurface.blit(kakeraImage,(j*pathwidth, path[j][i]))   #有判定過的圖
                if path[j][i] >= display_height and clickflag[j][i] == 0:           #未判定過而且落到底了的點
                    clickflag[j][i] = 1
                    Miss += 1
                    Combo = 0
        pygame.draw.rect(windowSurface, HpFrame,[display_width * 2/3 +30, 20, display_width / 3 - 50, 80])              #畫血條框
        pygame.draw.rect(windowSurface, YELLOW, [display_width * 2 / 3 + 35, 25, display_width / 3 - 60, 70])           #畫黃色血條
        if Miss <= 210:
            pygame.draw.rect(windowSurface, BLACK, [display_width - 25, 25, -(display_width / 3 - 60)*(Miss/210), 70])  #黑色方塊蓋掉黃色方塊 (扣血效果)
        else:
            pygame.draw.rect(windowSurface, BLACK, [display_width - 25, 25, -(display_width / 3 - 60), 70])

        if Miss + Hit >= 420:       #結束時間點
            music.stop()
            if Miss >= 210:
                startText = pygame.font.Font('LucidaBrightDemiBold.ttf', 100)
                TextSurf = startText.render('Fail', True, RED)
                TextRect = TextSurf.get_rect()
                TextRect.center = (display_width / 3, display_height / 2)
                windowSurface.blit(TextSurf, TextRect)
            else:
                startText = pygame.font.Font('LucidaBrightDemiBold.ttf', 100)
                TextSurf = startText.render('Complete', True, GREEN)
                TextRect = TextSurf.get_rect()
                TextRect.center = (display_width / 3, display_height / 2)
                windowSurface.blit(TextSurf, TextRect)

    pygame.display.update()
    pygame.time.Clock().tick(FPS)