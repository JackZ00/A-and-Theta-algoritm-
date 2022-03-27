import math
from tkinter import Tk, Canvas, Frame, BOTH, Label, Button, Toplevel
from array import *
import os
import numpy as np
from numpy import empty
from A_star import*

import sys






###test










   
   
   
   
   
   
   
   
   



































returnPath = returnPath


def getPath():
    absolutepath = os.path.abspath(__file__)
    print(absolutepath)
    fileDirectory = os.path.dirname(absolutepath)
    print(fileDirectory)
    #Navigate to Strings directory
    newPath = os.path.join(fileDirectory, 'mapfile/')
    print(newPath)
    return newPath

# read file,
#d = '/Users/liuqinyuan/Desktop/Rutgers Course/junior/cs440/assignment1/'
d = getPath()


# Put the square (x, x, x) into a 2d array
T = []
'''
for filename in os.listdir(d):
    if not filename.endswith('.txt'):
        continue

    with open(filename, 'r') as f:
        for line in f.readlines():
            T.append(line.split(' '))
'''
f = open(d+"mapcreate_for_i.txt", "r")
for line in f.readlines():
    T.append(line.split(' '))

# Change all the string to int in the 2d array
for i in range(len(T)):
    for j in range(len(T[i])):
        T[i][j] = int(T[i][j])

# Get start point
startPoint = T[0]
T = np.delete(T, 0, 0)
# Get goal point
goalPoint = T[0]
T = np.delete(T, 0, 0)
# Get total column and row
colRow = T[0]
T = np.delete(T, 0, 0)
#print(goalPoint)
#print(T)



'''
# 4x3
T = [[1, 1, 0], [1, 2, 0], [1, 3, 0], [1, 4, 0],
     [2, 1, 0], [2, 2, 1], [2, 3, 0], [2, 4, 0],
     [3, 1, 0], [3, 2, 0], [3, 3, 0], [3, 4, 0]]
#print(T[0][0])
'''

'''
Tblock  = [[0 for c in range(4)] for r in range(3)]
for i in range(len(Tblock)):
  for j in range(len(Tblock[i])):
    print(Tblock[i][j])
'''

root = Tk()
root.title('Assignment1')
root.geometry("5100x5100")
top = Toplevel()




# INPUT: how many in x, how many in y
Nx = colRow[0]; Ny = colRow[1];
gridSize = 15
# width, height distance
#Pwidth = Nx*gridSize; Pheight = Ny*gridSize
Pwidth = 2*Nx*(gridSize); Pheight = 2*Ny*gridSize


my_canvas = Canvas(root, width=Pwidth, height=Pheight)
my_canvas.pack()

x = 0; x1 = 0+gridSize
y = 0+gridSize; y1 = 0
i = 0; j = 0; r = 0


# adjust the value into the grid_size, in a bid to mach x,y value
for i in range(len(T)):
    for j in range(len(T[i])-1):
        T[i][j] = T[i][j]*gridSize
#    print(T[i])

# Draw the square
for i in range(len(T)):
    if (T[i][2]==1):
        my_canvas.create_rectangle(T[i][0]-gridSize, T[i][1]-gridSize, T[i][0], T[i][1], fill='gray')
    else:
        my_canvas.create_rectangle(T[i][0]-gridSize, T[i][1]-gridSize, T[i][0], T[i][1], fill='white')


# Draw start and goal point
my_canvas.create_oval(startPoint[0]*gridSize-gridSize-gridSize/5, startPoint[1]*gridSize-gridSize+gridSize/5,
                      startPoint[0]*gridSize-gridSize+gridSize/5, startPoint[1]*gridSize-gridSize-gridSize/5, width = 0, fill = 'red')
my_canvas.create_oval(goalPoint[0]*gridSize-gridSize-gridSize/5, goalPoint[1]*gridSize-gridSize+gridSize/5,
                      goalPoint[0]*gridSize-gridSize+gridSize/5, goalPoint[1]*gridSize-gridSize-gridSize/5, width = 0, fill = 'red')


# Draw a moving point
mov_pointX = gridSize
mov_pointY = gridSize

move_circle = my_canvas.create_oval(gridSize-gridSize/5, gridSize+gridSize/5, gridSize+gridSize/5, gridSize-gridSize/5, fill= 'blue')

# returnPath=[[4, 2], [3, 3], [2, 3], [0, 2]]
for i in range(len(returnPath)):
    for j in range(len(returnPath[i])):
        if (returnPath[i][j] != 0):
            returnPath[i][j] = returnPath[i][j]-1
        else:
            returnPath[i][j] = returnPath[i][j]


for i in range(len(returnPath)-1):
    my_canvas.create_line(returnPath[i][1]*gridSize, returnPath[i][0]*gridSize, returnPath[i+1][1]*gridSize, returnPath[i+1][0]*gridSize, fill="red")
    #print(returnPath[i+1][0])
    #print(returnPath[i])


#Move Function
def left(event):
    global mov_pointX, gridSize
    my_canvas.move(move_circle, -gridSize, 0)
    mov_pointX = mov_pointX-gridSize
def right(event):
    global mov_pointX, gridSize
    my_canvas.move(move_circle, gridSize, 0)
    mov_pointX = mov_pointX+gridSize
def up(event):
    global mov_pointY, gridSize
    my_canvas.move(move_circle, 0, -gridSize)
    mov_pointY = mov_pointY-gridSize
def down(event):
    global mov_pointY, gridSize
    my_canvas.move(move_circle, 0, gridSize)
    mov_pointY = mov_pointY+gridSize

# Get Value Function
def grab_value():
    global mov_pointX, mov_pointY, gridSize, startPoint, goalPoint

    starX = float(startPoint[0])-1
    starY = float(startPoint[1])-1
    movX = float(mov_pointX/gridSize)
    movY = float(mov_pointY/gridSize)
    endX = float(goalPoint[0])-1
    endY = float(goalPoint[1])-1

    #math.dist([Px, Py], [Qx, Qy])
    #h = math.sqrt(startPoint[0]**2 + (mov_pointX/gridSize)**2)
    # g(start->n) + h(n->goal)
    my_label_left.config(text="leftNode: " + str(math.dist([starX, starY], [movX-1, movY])) + " + " + str(math.dist([endX, endY], [movX-1, movY])))
    #print(starX, starY, movX, movY, endX, endY)
    my_label_right.config(text="RightNode: " + str(math.dist([starX, starY], [movX+1, movY])) + " + " + str(math.dist([endX, endY], [movX+1, movY])))
    my_label_up.config(text="upNode: " + str(math.dist([starX, starY], [movX, movY-1])) + " + " + str(math.dist([endX, endY], [movX, movY-1])))
    my_label_down.config(text="downNode: " + str(math.dist([starX, starY], [movX, movY+1])) + " + " + str(math.dist([endX, endY], [movX, movY+1])))

    my_label_topLeftCorner.config(text="topLeftCorner: " + str(math.dist([starX, starY], [movX-1, movY+1])) + " + " + str(math.dist([endX, endY], [movX-1, movY+1])))
    my_label_topRightCorner.config(text="topRightCorner: " + str(math.dist([starX, starY], [movX+1, movY+1])) + " + " + str(math.dist([endX, endY], [movX+1, movY+1])))
    my_label_lowerLeftCorner.config(text="lowerLeftCorner: " + str(math.dist([starX, starY], [movX-1, movY-1])) + " + " + str(math.dist([endX, endY], [movX-1, movY-1])))
    my_label_lowerRightCorner.config(text="lowerRightCorner: " + str(math.dist([starX, starY], [movX+1, movY-1])) + " + " + str(math.dist([endX, endY], [movX+1, movY-1])))

    my_label_center.config(text="center: " + str(math.dist([starX, starY], [movX, movY])) + " + " + str(math.dist([endX, endY], [movX, movY])))



my_button = Button(top, text="Get Value", command=grab_value)
my_button.pack(pady=10)
my_label_left = Label(top, text="")
my_label_left.pack(pady=5)
my_label_right = Label(top, text="")
my_label_right.pack(pady=5)
my_label_up = Label(top, text="")
my_label_up.pack(pady=5)
my_label_down = Label(top, text="")
my_label_down.pack(pady=5)

my_label_topLeftCorner = Label(top, text="")
my_label_topLeftCorner.pack(pady=5)
my_label_topRightCorner = Label(top, text="")
my_label_topRightCorner.pack(pady=5)
my_label_lowerLeftCorner = Label(top, text="")
my_label_lowerLeftCorner.pack(pady=5)
my_label_lowerRightCorner = Label(top, text="")
my_label_lowerRightCorner.pack(pady=5)

my_label_center = Label(top, text="")
my_label_center.pack(pady=5)

root.bind("<Left>", left)
root.bind("<Right>", right)
root.bind("<Up>", up)
root.bind("<Down>", down)
root.mainloop()