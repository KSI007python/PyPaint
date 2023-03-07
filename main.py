# This program belongs to Krishna Sai Jonnalgedda 

import pygame
import tkinter as tk
from tkinter import colorchooser
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import time

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((850, 800))

pygame.display.set_caption('PyPaint - Untitled.pypnt')

length = 70

brush_color = (0, 0, 0)

color_type = 'brush'

curr_tool = 'brush'

bg_color = (255, 255, 255)

brush_size = 2

eraser_size = 2

CanvasX, CanvasY = 150, 0

mouse_click = False

custom_color_ = None

pixelArray = [[bg_color for i in range(length)]for j in range(length)]

mirror = False

brush_tool_img = pygame.image.load('brush_tool.png')
paint_bucket_tool_img = pygame.image.load('paint_bucket_tool.png')
eraser_tool_img = pygame.image.load('eraser_tool.png')
color_picker_tool_img = pygame.image.load('color_picker_tool.png')
multicolor_img = pygame.image.load('custom_color_icon.jpg')
check_img = pygame.image.load('check.png')
icon_img = pygame.image.load('PaintIcon.png')
icon_img.set_colorkey((0, 0, 0))
pygame.display.set_icon(icon_img)

def drawtext(text, size, color, coors):
    font = pygame.font.Font('freesansbold.ttf', size)
    screen.blit(font.render(text, True, color), coors)

def change_color(color):

    if color_type == 'brush':
        global brush_color
        brush_color = color
    else:
        global bg_color
        bg_color = color


def canvas():
    curr_x = CanvasX
    curr_y = CanvasY
    for i in pixelArray:
        for j in i:
            pygame.draw.rect(screen, j, (curr_x, curr_y, 10, 10))
            curr_x += 10
        curr_x = CanvasX
        curr_y += 10

    for i in range(length+1):
        pygame.draw.line(screen, (0, 0, 0), (CanvasX+i*10, CanvasY), (CanvasX+i*10, CanvasY+length*10))
        pygame.draw.line(screen, (0, 0, 0), (CanvasX, CanvasY+i*10), (CanvasX+length*10, CanvasY+i*10))
    if mirror:
        pygame.draw.line(screen, (0, 0, 255), (CanvasX+length/2*10-1, CanvasY), (CanvasX+length/2*10-1, CanvasY+length*10), 3)

def draw(color):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    pixelY, pixelX = mouse_x // 10 - CanvasX // 10, mouse_y // 10 - CanvasY // 10

    if pixelX >= 0 and pixelX <= length and pixelY >= 0 and pixelY <= length and mouse_click:
        size = brush_size
        if curr_tool == 'eraser':
            size = eraser_size
        for i in range(size):
            for j in range(size):
                if pixelX+i < length and pixelY+j < length:
                    pixelArray[pixelX+i][pixelY+j] = color

                if mirror:
                    if pixelX+i < length and length-pixelY-j-1 < length+1:
                        pixelArray[pixelX+i][length-pixelY-j-1] = color


def color_palette(x, y):
    colors = [
        (0, 0, 0),
        (51, 51, 51),
        (100, 100, 100),
        (170, 170, 170),
        (255, 255, 255),
        (50, 0, 0),
        (100, 0, 0),
        (150, 0, 0),
        (200, 0, 0),
        (255, 0, 0),
        (0, 50, 0),
        (0, 100, 0), 
        (0, 150, 0),
        (0, 200, 0),
        (0, 255, 0),
        (0, 0, 50),
        (0, 0, 100),
        (0, 0, 150),
        (0, 0, 200),
        (0, 0, 255),
        (50, 50, 0),
        (100, 100, 0),
        (150, 150, 0),
        (200, 200, 0),
        (255, 255, 0),
        (50, 0, 50),
        (100, 0, 100),
        (150, 0, 150),
        (200, 0, 200),
        (255, 0, 255),
        (40, 0, 0),
        (70, 20, 0),
        (90, 40, 0),
        (100, 50, 30),
        (130, 80, 60)
    ]
    pygame.draw.rect(screen, (100, 100, 100), (x, y, 135, 215))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 135, 215), 1)
    curr_x = x+5
    curr_y = y+5
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for color in colors:
        if mouse_x > curr_x and mouse_x < curr_x + 25 and mouse_y > curr_y and mouse_y < curr_y + 25 and mouse_click:
            change_color(color)
        pygame.draw.rect(screen, color, (curr_x, curr_y, 25, 25))
        if (brush_color == color and color_type == 'brush') or (bg_color == color and color_type == 'eraser'):
            if color != (255, 255, 255) and color != (170, 170, 170) and color != (255, 255, 0) and color != (0, 255, 0):
                pygame.draw.rect(screen, (255, 255, 255), (curr_x, curr_y, 24, 25), 2)
            else:
                pygame.draw.rect(screen, (0, 0, 0), (curr_x, curr_y, 24, 25), 2)
        curr_x += 25
        if curr_x >= 125:
            curr_x = x+5
            curr_y += 30

def tool_box(x, y):
    pygame.draw.rect(screen, (100, 100, 100), (x, y, 115, 115))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 115, 115), 1)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    tools = {
        brush_tool_img : 'brush',
        eraser_tool_img : 'eraser',
        paint_bucket_tool_img : 'paint bucket',
        color_picker_tool_img : 'color picker'
    }
    curr_x = x + 5
    curr_y = y + 5
    for tool in tools.keys():
        inside = mouse_x > curr_x and mouse_x < curr_x + 50 and mouse_y > curr_y and mouse_y < curr_y + 50
        pygame.draw.rect(screen, (150, 150, 150), (curr_x, curr_y, 50, 50))
        if inside:
            pygame.draw.rect(screen, (120, 120, 120), (curr_x, curr_y, 50, 50))
            if mouse_click:
                global curr_tool 
                curr_tool = tools[tool]
        if curr_tool == tools[tool]:
            pygame.draw.rect(screen, (200, 200, 200), (curr_x, curr_y, 50, 50))
        pygame.draw.rect(screen, (0, 0, 0), (curr_x, curr_y, 50, 50), 1)
        screen.blit(pygame.transform.scale(tool, (40, 40)), (curr_x+5, curr_y+5))
        curr_x += 55
        if curr_x >= 110:
            curr_x = x + 5
            curr_y += 55

def fill(new_color):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pixelY, pixelX = mouse_x // 10 - CanvasX // 10, mouse_y // 10 - CanvasY // 10
    if pixelX >= 0 and pixelX < length and pixelY >= 0 and pixelY < length and mouse_click:
        replace_color = pixelArray[pixelX][pixelY]

        if replace_color == new_color:
            return

        q = [(pixelX, pixelY)]

        visited = []

        def check_valid(x, y):
            if x < 0 or x > length-1 or y < 0 or y > length-1:
                return False

            if pixelArray[x][y] != replace_color:
                return False

            if pixelArray[x][y] in visited:
                return False

            return True  
        while (q != []):
            x1, y1 = q.pop()
            pixelArray[x1][y1] = new_color

            moves = [
                (x1+1, y1),
                (x1, y1+1),
                (x1-1, y1),
                (x1, y1-1)
            ]

            visited.append((x1, y1))

            for move in moves:
                if check_valid(move[0], move[1]):
                    q.append(move)

        time.sleep(0.2)

def custom_color(x, y):
    def choose_color():
        root = tk.Tk()
        root.withdraw()
        color = colorchooser.askcolor()
        if color[0] != None:
            change_color(color[0])

        global custom_color_
        if color[0] != None:
            custom_color_ = color[0]
        global mouse_click
        mouse_click = False
        time.sleep(0.2)


    drawtext('custom', 20, (255, 255, 255), (x, y-20))

    pygame.draw.rect(screen, (100, 100, 100), (x, y, 70, 100))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 70, 100), 1)

    pygame.draw.rect(screen, (0, 0, 0), (x+10, y+5, 50, 50), 1)

    if (brush_color == custom_color_ and color_type == 'brush') or (bg_color == custom_color_ and color_type == 'eraser'):
        pygame.draw.rect(screen, (255, 255, 255), (x+10, y+5, 50, 50), 3)

        

    if custom_color_ != None:
        pygame.draw.rect(screen, custom_color_, (x+15, y+10, 40, 40))
    else:
        pygame.draw.rect(screen, (0, 0, 0), (x+15, y+10, 40, 40), 1)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    inside = mouse_x > x + 10 and mouse_x < x + 60 and mouse_y > y + 60 and mouse_y < y + 90

    if inside:
        pygame.draw.rect(screen, (90, 90, 90), (x+10, y+60, 50, 30))
        if mouse_click:
            choose_color()

    inside2 = mouse_x > x + 15 and mouse_x < x + 55 and mouse_y > y + 10 and mouse_y < y + 50
    if inside2 and mouse_click and custom_color_ != None:
        change_color(custom_color_)

    screen.blit(pygame.transform.scale(multicolor_img, (40, 20)), (x+15, y+65))

def color_picker():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pixelY, pixelX = mouse_x // 10 - CanvasX // 10, mouse_y // 10 - CanvasY // 10

    if mouse_x > CanvasX and mouse_x < CanvasX + length*10 and mouse_y > CanvasY and mouse_y < CanvasY + length*10 and mouse_click:
        change_color(pixelArray[pixelX][pixelY])
        global curr_tool
        if color_type == 'brush':
            curr_tool = 'brush'
        else:
            curr_tool = 'eraser'
        time.sleep(0.2)

def slider(x, y, mode):
    pygame.draw.rect(screen, (100, 100, 100), (x+5, y+47, 110, 6))
    drawtext(mode+' size', 20, (255, 255, 255), (x+10, y+15))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    global brush_size
    global eraser_size
    if mode == 'brush':
        curr_pos = brush_size*20
    else:
        curr_pos = eraser_size*20
    for i in range(5):
        if mouse_x > x+5+i*20 and mouse_x < x+30+i*20 and mouse_y > y+40 and mouse_y < y+60 and mouse_click:
            if mode == 'brush':
                brush_size = i+1
            else:
                eraser_size = i+1
    pygame.draw.rect(screen, (150, 150, 150), (x+curr_pos-5, y+40, 10, 20))

def mirror_button(x, y):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    inside = mouse_x > x and mouse_x < x+130 and mouse_y > y and mouse_y < y+50
    pygame.draw.rect(screen, (100, 100, 100), (x, y, 130, 50))
    if inside:
        pygame.draw.rect(screen, (80, 80, 80), (x, y, 130, 50))
        if mouse_click:
            global mirror
            if mirror:
                mirror = False
            else:
                mirror = True
            time.sleep(0.2)
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 130, 50), 2)
    drawtext('mirror', 20, (0, 0, 0), (x+10, y+15))
    pygame.draw.rect(screen, (150, 150, 150), (x+85, y+5, 40, 40))
    if mirror:
        screen.blit(pygame.transform.scale(check_img, (40, 40)), (x+85, y+5))

def color_box(x, y):
    pygame.draw.rect(screen, (150, 150, 150), (x, y, 178, 83))
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 178, 83), 1)
    pygame.draw.rect(screen, brush_color, (x+10, y+10, 63, 63))
    pygame.draw.rect(screen, bg_color, (x+105, y+10, 63, 63))
    pygame.draw.rect(screen, (0, 0, 0), (x+5, y+5, 73, 73), 1)
    pygame.draw.rect(screen, (0, 0, 0), (x+100, y+5, 73, 73), 1)
    global color_type
    if color_type == 'brush':
        pygame.draw.rect(screen, (255, 255, 255), (x+5, y+5, 73, 73), 2)
    else:
        pygame.draw.rect(screen, (255, 255, 255), (x+100, y+5, 73, 73), 2)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_x > x+10 and mouse_x < x+73 and mouse_y > y+10 and mouse_y < y+73 and mouse_click:
        color_type = 'brush'
    if mouse_x > x+105 and mouse_x < x+178 and mouse_y > y+10 and mouse_y < y+73 and mouse_click:
        color_type = 'eraser'

def Save():
    root = tk.Tk()
    root.withdraw()
    fname = asksaveasfilename(title='Save', defaultextension='.pypnt', filetypes=[('PyPaint', '.pypnt')])
    if fname != '':
        f = open(fname, 'w')
        str_pixelArray = ''
        for i in pixelArray:
            str_pixelArray += str(i) + '\n'
        f.write(str_pixelArray)
        pygame.display.set_caption("PyPaint - " + fname.split('/')[-1])

def Open():
    root = tk.Tk()
    root.withdraw()
    fname = askopenfilename(title='Open', filetypes = [('pypaint', '.pypnt')])
    print(fname == '')
    if fname != '':
        f = open(fname, 'r')
        new_pixelArray = []
        for i in f.readlines():
            new_pixelArray.append(eval(i))
        pygame.display.set_caption("PyPaint - " + fname.split('/')[-1])
        global pixelArray
        pixelArray = new_pixelArray

def Capture():
    picture = pygame.Surface((700, 700))
    for i in range(length):
        for j in range(length):
            pygame.draw.rect(picture, pixelArray[j][i], (i*10, j*10, 10, 10))
    root = tk.Tk()
    root.withdraw()
    fname = asksaveasfilename(title='Capture',defaultextension='.png', filetypes=[('Portable Network Graphics','.png'), ('Joint Photographic Experts Group', '.jpg')])
    if fname != '':
        pygame.image.save(picture, fname)
    time.sleep(0.2)
running = True

def clear():
    global pixelArray
    pixelArray = [[bg_color for i in range(length)]for j in range(length)]

def button(x, y, text, command = lambda : None):
    pygame.draw.rect(screen, (150, 150, 150), (x, y, 100, 70))
    mouse_x, mouse_y = pygame.mouse.get_pos()
    inside = mouse_x > x and mouse_x < x + 100 and mouse_y > y and mouse_y < y + 70
    if inside:
        pygame.draw.rect(screen, (120, 120, 120), (x, y, 100, 70))
        if mouse_click:
            command()
    pygame.draw.rect(screen, (0, 0, 0), (x, y, 100, 70), 2)
    drawtext(text, 20, (0, 0, 0), (x+10, y+23))

def change_cursor():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    inside = mouse_x > CanvasX and mouse_x < CanvasX+length*10-10 and mouse_y > CanvasY and mouse_y < CanvasY+length*10-10
    if inside:
        pygame.mouse.set_visible(False)
        if curr_tool == 'brush':
            pygame.draw.ellipse(screen, brush_color, (mouse_x-5, mouse_y-5, brush_size*10, brush_size*10))
            if brush_color[0] < 100 and brush_color[1] < 100 and brush_color[2] < 100:
                pygame.draw.ellipse(screen, (255, 255, 255), (mouse_x-5, mouse_y-5, brush_size*10, brush_size*10), 1)
            else:
                pygame.draw.ellipse(screen, (0, 0, 0), (mouse_x-5, mouse_y-5, brush_size*10, brush_size*10), 1)
        if curr_tool == 'eraser':
            pygame.draw.ellipse(screen, bg_color, (mouse_x-5, mouse_y-5, eraser_size*10, eraser_size*10))
            if bg_color[0] < 100 and bg_color[1] < 100 and bg_color[2] < 100:
                pygame.draw.ellipse(screen, (255, 255, 255), (mouse_x-5, mouse_y-5, eraser_size*10, eraser_size*10), 1)
            else:
                pygame.draw.ellipse(screen, (0, 0, 0), (mouse_x-5, mouse_y-5, eraser_size*10, eraser_size*10), 1)
        if curr_tool == 'paint bucket':
            screen.blit(pygame.transform.scale(paint_bucket_tool_img, (30, 30)), (mouse_x-30, mouse_y-25))
        if curr_tool == 'color picker':
            screen.blit(pygame.transform.scale(color_picker_tool_img, (30, 30)), (mouse_x, mouse_y-25))
    else:
        pygame.mouse.set_visible(True)

while running:

    screen.fill((50, 50, 50))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            root = tk.Tk()
            root.withdraw()
            want_to_save = messagebox.askquestion(title='Save', message='Do you want to save your work?')
            if want_to_save == 'yes':
                Save()
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_click = False

    canvas()

    pygame.draw.rect(screen, (30, 30, 30), (2, 2, 145, 797))

    if curr_tool == 'brush':
        draw(brush_color)

    if curr_tool == 'eraser':
        draw(bg_color)

    if curr_tool == 'paint bucket':
        fill(brush_color)

    if curr_tool == 'color picker':
        color_picker()

    color_palette(7, 5)

    tool_box(15, 390)

    custom_color(40, 260)

    slider(10, 530, 'brush')

    slider(10, 600, 'eraser')

    mirror_button(10, 705)

    color_box(170, 710)

    button(400, 717, '  Clear', clear)

    button(505, 717, '  Save', Save)

    button(610, 717, '  Open', Open)

    button(715, 717, 'Capture', Capture)
    
    change_cursor()

    pygame.display.update()
