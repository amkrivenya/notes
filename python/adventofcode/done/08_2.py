#!/usr/bin/python
import os
from datetime import datetime

start_time = datetime.now()

# Initializing
SIZE = 99
tree = [[0 for j in range(SIZE)] for i in range(SIZE)]
can_see = [0]*4
can_see_max = 0

# Readind file with trees in array
input_file = open('08_in.txt', mode="r")

row = 0
for line in input_file:
    line = line.replace('\r', ''); line = line.replace('\n', '')
    for clm in range(len(line)): tree[row][clm] = int(line[clm])
    row += 1

input_file.close()

# Looking for visible trees in four directions
for row in range(len(tree)):
    for clm in range(len(tree[0])):

        # Looking for visible trees in left direction
        for i in range(clm-1, -1, -1):
            if tree[row][clm] > tree[row][i]: can_see[0] += 1
            else: can_see[0] += 1; break

        # Looking for visible trees in right direction
        for i in range(clm+1, len(tree[0])):
            if tree[row][clm] > tree[row][i]: can_see[1] += 1
            else: can_see[1] += 1; break

        # Looking for visible trees in up direction
        for i in range(row-1, -1, -1):
            if tree[row][clm] > tree[i][clm]: can_see[2] += 1
            else: can_see[2] += 1; break

        # Looking for visible trees in down direction
        for i in range(row+1, len(tree)):
            if tree[row][clm] > tree[i][clm]: can_see[3] += 1
            else: can_see[3] += 1; break

        if can_see_max < can_see[0]*can_see[1]*can_see[2]*can_see[3]: 
            can_see_max = can_see[0]*can_see[1]*can_see[2]*can_see[3] 
#            print(can_see, can_see_max, row, clm, tree[row][clm])
                      
        can_see = [0]*4

print('Highest scenic score:', can_see_max)
print('Time to execute:', str(datetime.now() - start_time))

