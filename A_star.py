from math import  sqrt
import timeit

from matplotlib.pyplot import close

"""
#Hypotenuse
def hypo(x, y):
    return sqrt(x ** 2 + y ** 2)
"""

# read file
# define
returnPath = []

def readfile(filepath):
    Maze =[]

    with open(filepath, 'r') as f:
        for line in f.readlines():
            Maze.append(line.split(' '))
    for i in range(len(Maze)):
        for j in range(len(Maze[i])):
            Maze[i][j] = int(Maze[i][j])
    return Maze

# For h-values of A* algorithm
def h(x_cur_node,x_end_node,y_cur_node,y_end_node):
    return sqrt(2)*min(abs(x_cur_node-x_end_node),abs(y_cur_node-y_end_node))+max(abs(x_cur_node-x_end_node),abs(y_cur_node-y_end_node))-min(abs(x_cur_node-x_end_node),abs(y_cur_node-y_end_node))

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
                if j == 2:
                    block[i-1][j-2] =2
                if i == (len(block) -1):
                    block[i][j-1] =2
                if i == 2:
                    block[i-2][j-1] =2


                if block[i][j-2] == 1:
                    block[i-1][j-2] = 2
                elif block[i-2][j] == 1:
                    block[i-2][j-1] =2
                
                    
    return block

class Node():

    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.position = position
        self.parent = parent

        self.f = 0
        self.g = 0
        self.h = 0


    def __eq__(self, other):
        return self.position == other.position

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
    fringe = []
    closed = []

    # Add the start node
    fringe.append(START)

    # Loop until you find the end
    while len(fringe) > 0:

        # Get the current node
        current_node = fringe[0]
        current_index = 0
        for index, item in enumerate(fringe):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # print(current_node)
        # print(current_index)
       
        # print(fringe)
        # Pop current off open list, add to closed list
        fringe.pop(current_index)
        closed.append(current_node)

        # print(fringe)
        # print(closed)

        # Found the goal
        if current_node == END:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        
        # Loop through children
        for child in children(current_node,maze):

            # Child is on the closed list
            for closed_child in closed:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            if child.position[0] in [2,-2] and child.position[1] in [2,-2]:
                child.g = current_node.g + sqrt(2)
            else:
                child.g = current_node.g + 2
            child.h = h(child.position[0],END.position[0],child.position[1],END.position[1])
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in fringe:
                if child.g > open_node.g and child == open_node:
                    continue

            # Add the child to the open list
            fringe.append(child)
        
        


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
    print('A* Algorithm Run Time: ', stop1 - start1) 

# def getReturnPath():

#     print("here")
#     print(returnPath)
#     return returnPath
#getReturnPath()








