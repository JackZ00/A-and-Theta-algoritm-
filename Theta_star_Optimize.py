from math import  sqrt
import timeit
from numpy import empty

from sklearn import neighbors

#Hypotenuse
def hypo(x, y):
    return sqrt(x ** 2 + y ** 2)

#list to arry 
def list2array(path):
    returnPath = [[0 for c in range(len(path[0]))] for r in range(len(path))]
    for i in range(len(path)):
         for j in range(len(path[i])):
             returnPath[i][j] = int(path[i][j])
    return returnPath

# read file
def readfile(filepath):
    Maze =[]

    with open(filepath, 'r') as f:
        for line in f.readlines():
            Maze.append(line.split(' '))
    for i in range(len(Maze)):
        for j in range(len(Maze[i])):
            Maze[i][j] = int(Maze[i][j])
    return Maze

#Generate map with blocked
def blockMaze(Maze,row, column):

    block  = [[0 for c in range(row+row+1)] for r in range(column+column+1)]
    
    for i in Maze[3:]:
        if i[2] == 1:
            block[(i[1])+(i[1])][(i[0])+(i[0])] = 1

    for i in range(len(block)):
        for j in range(len(block[i])):
            if block[i][j] == 1:
                block[i-1][j-1] =2
                if j == (len(block[len(block)-1]) -1) : 
                    block[i-1][j] =2
                elif j == 2: 
                    block[i-1][j-2] =2
                elif i == (len(block) -1):
                    block[i][j-1] =2
                elif i == 2:
                    block[i-2][j-1] =2


                if block[i][j-2] == 1:
                    block[i-1][j-2] = 2
                elif block[i-2][j] == 1:
                    block[i-2][j-1] =2
    return block


class MinHeap:

    def __init__(self):
        self.fringe = []

    # method for adding the givenItem to the heap
    def insert(self, givenItem):
        self.fringe.append(givenItem)
        self.heapify()

    #method for deleting minmun value in the heap
    def delete(self):
        self.fringe.pop(0)
        self.heapify()

    # method for getting the deep copy of the heap list
    def getHeap(self):
        return self.fringe


    # method to change the position of the elements in the heap in order to satisfy the heap property
    def heapify(self):

        for item in range(len(self.fringe)):

            # if the index is greater than or equal to 1 and the parent is greater than children, then swap
            while item >= 1 and self.fringe[item].f <= self.fringe[item//2].f:

                if self.fringe[item].f < self.fringe[item//2].f:

                    self.swap(self.fringe, item, item // 2)

                elif self.fringe[item].f == self.fringe[item//2].f:

                    if self.fringe[item].h < self.fringe[item//2].h:

                        self.swap(self.fringe, item, item // 2)

                item = item // 2

    # method to get the minimum item from the heap
    def getMin(self):
        return self.fringe[0]

    # method for swapping the values in the heap
    def swap(self, fringe, index1, index2):
        tempVal = fringe[index1]
        fringe[index1] = fringe[index2]
        fringe[index2] = tempVal

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.position = position
        self.parent = parent

        self.f = 0
        self.g = 0
        self.h = 0


# Generate children
def children(current_node,maze):
        children = []
        for new_position in [(0, -2), (0, 2), (-2, 0), (2, 0), (-2, -2), (-2, 2), (2, -2), (2, 2)]: # Adjacent squares

            if new_position == (0, -2):
                gap_position = [0, -1]
            elif new_position == (0, 2):
                gap_position = [0, 1]
            elif new_position == (-2, 0):
                gap_position = [-1, 0]
            elif new_position == (2, 0):
                gap_position = [1, 0]
            elif new_position == (-2, -2):
                gap_position = [-1, -1]
            elif new_position == (-2, 2):
                gap_position = [-1, 1]
            elif new_position == (2, -2):
                gap_position = [1, -1]
            elif new_position == (2, 2):
                gap_position = [1, 1]

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            node_gap_position = (current_node.position[0] + gap_position[0], current_node.position[1] + gap_position[1])

            # Make sure within range
            if node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0 or node_position[0] > (len(maze) - 1) or node_position[0] < 0:
                continue

            # Make sure walkable terrain
            
            if maze[node_gap_position[0]][node_gap_position[1]] == 2 :
                continue
            

            # Create and append new node
            new_node = Node(current_node, node_position)
            children.append(new_node)

        return children

def LineOfSight(cur,child,grid):
    x0 = cur.position[0]
    y0 = cur.position[1]
    x1 = child.position[0]
    y1 = child.position[1]
    sx = 0
    sy = 0
    f = 0
    dy = y1 - y0
    dx = x1 - x0
    if dy < 0 :
        dy = -dy
        sy = -1
    else:
        sy = 1
    
    if dx < 0 :
        dx = -dx
        sx = -1
    else:
        sx = 1
    if dx >= dy :
        while x0 != x1 :
            f = f +dy
            if f >= dy:
                if grid[int(x0 +((sx-1)/2))][ int(y0 +((sy - 1)/2))] == 2:
                    return False
                y0 = y0 + sy
                f = f - dx
            if f != 0  and grid[int(x0 +((sx-1)/2))][ int(y0 +((sy - 1)/2))] ==2 :
                return False
            if dy == 0 and grid[int(x0 +((sx-1)/2))][ y0] ==2 and grid[int(x0 +((sx-1)/2))][ y0 -1] ==2:
                return False
            x0 = x0 + sx
    else:
        while y0  != y1 :
            f = f + dx
            if f >= dy:
                if grid[int(x0 +((sx-1)/2))][ int(y0 +((sy -1)/2))] == 2:
                    return False
                x0 = x0 + sx
                f = f - dy
            if f != 0 and grid[int(x0 +((sx-1)/2))][ int(y0 +((sy -1)/2))]==2:
                return False
            if dx == 0 and grid[x0][int(y0+((sy -1)/2))] == 2 and grid[x0-1][int(y0+((sy -1)/2))] ==2:
                return False
            y0 = y0 +sy
    return True

# A* algorithm
def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    #Generate start and end 
    START = Node(None, start)
    END = Node(None, end)
    START.g = 0
    START.h = 0
    START.f = 0
    END.g = 0
    END.h = 0
    END.f = 0

    # Initialize both open and closed list
    fringe = MinHeap()
    closed = []

    # Add the start node
    fringe.insert(START)

    # Loop until you find the end
    while len(fringe.getHeap()) != 0:
        current_node = fringe.getMin()
        current_node1 = current_node.position

        # Get the current node
        # current_node = fringe[0]
        # current_index = 0
        # for index, item in enumerate(fringe):
        #     if item.f < current_node.f:
        #         current_node = item
        #         current_index = index

        # Pop current off open list, add to closed list
        fringe.delete()
        # print(fringe.getHeap())
        if current_node1 not in closed:
            closed.append(current_node1)
        # print(closed)
        
        # Found the goal and return the path
        # if current_node == end:
        #     path = []
        #     # start1 = closed[0]
        #     current = current_node
        #     closed.append(END)
        #     for i in range(len(closed)-1):
        #         path.append((closed[i].position[0],closed[i].position[1]))
        #     current = current.parent
        #     return path
        # print(closed[-1], ' ', type(closed[-1]))
        # print (end, ' ', type(end))
        if closed[-1] == end:
                path = []
                current = current_node
                # for index, item in enumerate(closed):
                #     if item == choice and LineOfSight (choice,END,maze) == True:
                #         if index+1 <= len(closed)-1:
                #             closed.pop(index+1)
                closed.append(END)
                for i in range(len(closed)-1):
                    path.append(closed[i])
                    # print(path)
                current = current.parent
                return path


        # print('cur_node:      ', current_node.position[0], ' ',current_node.position[1])
        # Loop through children
        for child in children(current_node,maze):

            
            if current_node == START :
                child.parent = current_node.parent = START
            # Child is on the closed list
            if child not in closed:
                # Child is already in the open list
                if child not in fringe.getHeap():

                    # print('closed: ',closed[len(closed)-1].position[0],' ',closed[len(closed)-1].position[1])
                    if LineOfSight (current_node.parent,child,maze) == True:
                        # Create the f, g, and h values
                        child.g = hypo(abs(child.position[0]-current_node.parent.position[0]),abs(child.position[1]-current_node.parent.position[1]))
                        child.h = hypo(abs(child.position[0]-END.position[0]),abs(child.position[1]-END.position[1]))
                        child.f = child.g + child.h   

                        # choice = current_node.parent    

                    else:
                        # Create the f, g, and h values
                        child.g = hypo(abs(child.position[0]-current_node.position[0]),abs(child.position[1]-current_node.position[1]))
                        child.h = hypo(abs(child.position[0]-END.position[0]),abs(child.position[1]-END.position[1]))
                        child.f = child.g + child.h
                        # print('current_node: ', current_node.position[0],' ',current_node.position[1] )
                        # choice = current_node.parent
                       
                        # child.parent = current_node
                    # print('------')
                    # print('-',fringe.getHeap())                        
                    for open_node in fringe.getHeap():
                # print(child.position,open_node.position )
                        # print(child.position,open_node.position )
                        if child.g > open_node.g and (child.position[0] == open_node.position[0] and child.position[1] == open_node.position[1]):
                            continue

                    # Add the child to the open list
                    
                    fringe.insert(child)
                        
                    # Add the child to the open list
                    
            
            
            # for i in range(len(fringe.getHeap())-1):
            #     print('closed_node:      ', closed[i].position[0], ' ',closed[i].position[1])
            # print('\n')
        # for i in range(len(fringe.getHeap())-1):
        #         print('open_node:      ', fringe.getHeap()[i].position[0], ' ',fringe.getHeap()[i].position[1],' ',fringe.getHeap()[i].g,' ',fringe.getHeap()[i].h,' ',fringe.getHeap()[i].f)
            
    raise ValueError('No Path Found')

if __name__ == '__main__':

    # Get value from file
    value = 'assignment1/value.txt'
    Maze = readfile(value)

    # Get the size of Map
    row = Maze[2][0]
    column = Maze[2][1]

    # Get star and end node
    start = (int(Maze[0][1])+int(Maze[0][1])-2,int(Maze[0][0])+int(Maze[0][0])-2)
    end = (int(Maze[1][1])+int(Maze[1][1])-2,int(Maze[1][0])+int(Maze[1][0])-2)
    # print(start)
    # print(end)

    # Generate the Map with block
    maze = blockMaze(Maze,row,column)

    # Mark the star and goal in Map
    maze[int(Maze[0][1])+int(Maze[0][1])-2][int(Maze[0][0])+int(Maze[0][0])-2] ='s'
    maze[int(Maze[1][1])+int(Maze[1][1])-2][int(Maze[1][0])+int(Maze[1][0])-2] = 'g'


    # Print Map
    # for i in range(len(maze)):
    #     print(maze[i])

    start1 = timeit.default_timer()
    # Get path
    path = astar(maze, start, end)
    # print(path)
    stop1 = timeit.default_timer()

    #path1 = [[0,0], [0,0], [0,0], [0,0]]
    returnPath = [[0 for c in range(len(path[0]))] for r in range(len(path))]
    for i in range(len(path)):
         for j in range(len(path[i])):
             returnPath[i][j] = int(path[i][j])

    # print(returnPath)
    for i in range(len(returnPath)):
         for j in range(len(returnPath[i])):
            if ((returnPath[i][j]!=0)and(returnPath[i][j]!=1)):
                returnPath[i][j] = int((path[i][j]+2)/2)
            else:
                returnPath[i][j] = returnPath[i][j]
    print(returnPath)
    """ the index 0 = 1 in the returnPath"""
    print('Theta* Algorithm Run Time After Optimize: ', stop1 - start1) 
   