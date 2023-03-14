#!/usr/bin/python
import os
from datetime import datetime
#import time

start_time = datetime.now()


def head_move(direction, length):
    return

# Initializing
SIZE = 30
bridge = [[0 for j in range(SIZE)] for i in range(SIZE)]

# Readind file with trees in array
input_file = open('09_in.txt', mode="r")

head_clm=15
head_row=15

if True:
    bridge[head_row][head_clm] = 1
    for i in range(SIZE):
        for j in range(SIZE):
            print(bridge[i][j], end='')
        print()
    print(head_row, head_clm)

for line in input_file:
    
    line = line.replace('\r', ''); line = line.replace('\n', '')

    dir = line[0]
    if len(line) == 4: length = int(line[2] + line[3])
    else: length = int(line[2])

    print(line,'     ', dir, length)

    bridge[head_row][head_clm] = 1

    if line[0] == 'U': head_row = head_row - length
    if line[0] == 'D': head_row = head_row + length
    if line[0] == 'L': head_clm = head_clm - length
    if line[0] == 'R': head_clm = head_clm + length

    bridge[head_row][head_clm] = 5

    input()

#    time.sleep(2.1)
    os.system('cls||clear')
#    print(bridge)

    for i in range(SIZE):
        for j in range(SIZE):
            print(bridge[i][j], end='')
        print()
    print(head_row, head_clm)




input_file.close()

print('Time to execute:', datetime.now() - start_time)

