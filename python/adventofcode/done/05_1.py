#!/usr/bin/python
import os
import array

vcFile='05_in.txt'
vfFile = open(vcFile, mode="r")

#amk=["",""]
amk=[[0 for j in range(9)] for i in range(45)]

l = 8
for line in vfFile:

  if l > 0:
    for i in [1,5,9,13,17,21,25,29,33]:
      if ord( line[i] ) >= ord('A') and ord( line[i] ) <= ord('Z'):
        amk[l-1][(i-1)//4] = ord( line[i] )
    l = l - 1

  if line[0] == 'm':

    im = int(line[5 : 7] )
    ifr = int(line[line.rfind("f") + 5 : line.rfind("f") + 7]) - 1
    it = int(line[line.rfind("t") + 3]) - 1

    if 1:
      ifrMax = 0
      while amk[ifrMax][ifr] >= ord('A') and amk[ifrMax][ifr] <= ord('Z') and ifrMax < len(amk): ifrMax = ifrMax + 1
      ifrMax = ifrMax - 1

      itMax = 0
      while amk[itMax][it] >= ord('A') and amk[itMax][it] <= ord('Z') and itMax <= len(amk): itMax = itMax + 1
      itMax = itMax - 1

      i = 1
      while i <= im:
        amk[itMax + i][it] = amk[ifrMax + 1 - i][ifr]
        amk[ifrMax + 1 - i][ifr] = 0
        i=i+1

for i in range(9):
  for j in range(len(amk)):
    if ( amk[j][i] != 0 and amk[j+1][i] == 0 ): print (chr(amk[j][i]),end ="")

vfFile.close()
