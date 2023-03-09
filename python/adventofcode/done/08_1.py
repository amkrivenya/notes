#!/usr/bin/python
import os
from datetime import datetime

start_time = datetime.now()

# Initializing arrays
SIZE = 99
visiblle = [[0 for j in range(SIZE)] for i in range(SIZE)]
tree = [[0 for j in range(SIZE)] for i in range(SIZE)]

# Readind file with trees in array
input_file = open('08_in.txt', mode="r")

i_line = 0
for line in input_file:
    line = line.replace('\r', ''); line = line.replace('\n', '')
    for i in range(len(line)): tree[i_line][i] = int(line[i])
    i_line += 1

input_file.close()

# Looking for trees in horizontal direction
for i in range(len(tree)):

    # Looking for trees that visible from left to right
    last_visible = 0
    for k in range(len(tree[i])):
        if k == 0: visiblle[i][k] = 1
        if last_visible < tree[i][k]:
            last_visible = tree[i][k]
            visiblle[i][k] = 1

    # Looking for trees that visible from right to left
    last_visible = 0
    for k in range(len(tree), -1, -1):
        if k == len(tree[i]): visiblle[i][k-1] = 1
        else:
            if last_visible < tree[i][k]:
                last_visible = tree[i][k]
                visiblle[i][k] = 1

# Looking for trees in vertical direction
for k in range(len(tree[0])):

    # Looking for trees that visible from up to down
    last_visible = 0
    for i in range(len(tree)):
        if i == 0: visiblle[i][k] = 1
        if last_visible < tree[i][k]:
            last_visible = tree[i][k]
            visiblle[i][k] = 1

    # Looking for trees that visible from down to up
    last_visible = 0
    for i in range(len(tree), -1, -1):
        if i == len(tree[i-1]): visiblle[i-1][k] = 1
        else:
            if last_visible < tree[i][k]:
                last_visible = tree[i][k]
                visiblle[i][k] = 1

# Counting visible trees
summ_trees = 0
for i in range(len(visiblle)):
    for j in range(len(visiblle[i])):
        if visiblle[i][j] > 0: summ_trees += 1
# For printing visible trees
#        print(visiblle[i][j], end='')
#    print()

print('Number of visible trees:', summ_trees)
print('Time to execute:', str(datetime.now() - start_time))
