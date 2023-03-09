#!/usr/bin/python
import os

vcFile='02_in.txt'
vfFile = open(vcFile, mode="r")

vCurrent=0

for line in vfFile:
           
  if line[2] == 'X':
    vCurrent = vCurrent + 0
    if line[0] == 'A': vCurrent = vCurrent + 3
    if line[0] == 'B': vCurrent = vCurrent + 1
    if line[0] == 'C': vCurrent = vCurrent + 2
                                             
  if line[2] == 'Y':
    vCurrent = vCurrent + 3
    if line[0] == 'A': vCurrent = vCurrent + 1
    if line[0] == 'B': vCurrent = vCurrent + 2
    if line[0] == 'C': vCurrent = vCurrent + 3

  if line[2] == 'Z':
    vCurrent = vCurrent + 6
    if line[0] == 'A': vCurrent = vCurrent + 2
    if line[0] == 'B': vCurrent = vCurrent + 3
    if line[0] == 'C': vCurrent = vCurrent + 1

print(vCurrent);
vfFile.close()