#!/usr/bin/python
import os

vcFile='01_in.txt'
vfFile = open(vcFile, mode="r")

vBigger=0
vCurrent=0

for line in vfFile:

  if len(line) == 1:
    if vBigger < vCurrent: vBigger = vCurrent
    vCurrent = 0

  else:
    vCurrent = vCurrent + int(line)    

print(vBigger);
vfFile.close()