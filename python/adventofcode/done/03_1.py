#!/usr/bin/python
import os

vcFile='03_in.txt'
vfFile = open(vcFile, mode="r")

vCurrent=0

for line in vfFile:
  line = line.replace('\r', '')            
  ifFound=0

  i=0
  while ( i < len(line)//2 and ifFound==0 ):
    j = len(line) // 2
    while ( j < len(line) and ifFound==0 ):   
      if ( line[i] == line[j] ):
        ifFound = 1
        if line[i].islower(): vCurrent = vCurrent + ord( line[i] ) - ord('a') + 1 
        if line[i].isupper(): vCurrent = vCurrent + ord( line[i] ) - ord('A') + 27 

      j=j+1
    i=i+1

print(vCurrent);
vfFile.close()