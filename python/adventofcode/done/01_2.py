#!/usr/bin/python
import os

vcFile='01_in.txt'
vfFile = open(vcFile, mode="r")

vBigger=0
vBigger2=0
vBigger3=0

vCurrent=0

for line in vfFile:

  if len(line) == 1:

     if vBigger < vCurrent: vBigger3 = vBigger2; vBigger2 = vBigger; vBigger = vCurrent
     else:
       if vBigger2 < vCurrent: vBigger3 = vBigger2; vBigger2 = vCurrent
       else:
         if vBigger3 < vCurrent: vBigger3 = vCurrent

     vCurrent = 0

  else:
    vCurrent = vCurrent + int(line)    

vCurrent = vBigger + vBigger2 + vBigger3

print(vCurrent)
vfFile.close()
