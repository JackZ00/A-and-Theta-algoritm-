import random
import os

##
import sys

absolutepath = os.path.abspath(__file__)
#print(absolutepath)
fileDirectory = os.path.dirname(absolutepath)
#print(fileDirectory)
#Path of parent directory

#Navigate to Strings directory
newPath = os.path.join(fileDirectory, 'mapfile')
#print(newPath)

file1 = open(newPath+"/mapcreate_for_i.txt", "w")
##

#file1 = open("/Users/liuqinyuan/Desktop/Rutgers Course/大三 下/cs440/assignment1/mapcreate.txt", "w")

# mapSize
L = [str(6)+" ", str(4)+"\n"]
# start and end point
startX = random.randint(1, 7)
startY = random.randint(1, 5)
endX = random.randint(1, 7)
endY = random.randint(1, 5)


file1.writelines([str(startX)+" ", str(startY)+"\n"])
file1.writelines([str(endX)+" ", str(endY)+"\n"])
file1.writelines(L)
# generate each box
for i in range(1, 7):
    for j in range(1, 5):
        guess = random.randint(1, 101)
        if (guess>=10):
            file1.writelines([str(i)+" ", str(j)+" ", "0\n"])
        else:
            file1.writelines([str(i) + " ", str(j) + " ", "1\n"])


# \n is placed to indicate EOL (End of Line)




file1.close()  # t