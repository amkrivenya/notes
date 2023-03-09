#!/usr/bin/python
import os

vcFile='03_in.txt'
vfFile = open(vcFile, mode="r")

vCurrent=0
vGroup=0

for line in vfFile:
          
  if vGroup == 2: vElf3 = line; vGroup = 3
  if vGroup == 1: vElf2 = line; vGroup = 2
  if vGroup == 0: vElf1 = line; vGroup = 1

  ifFound=0

  if vGroup == 3:
    i=0
    while ( i < len( vElf1 ) and ifFound == 0 ):
      j=0
      while ( j < len( vElf2 ) and ifFound == 0 ):   
        if ( vElf1[i] == vElf2[j] ):

          k=0
          while ( k < len( vElf3 ) and ifFound == 0 ):   
            if ( vElf1[i] == vElf3[k] ):
              ifFound=1
              vGroup=0
              
              if vElf1[i].islower(): vCurrent = vCurrent + ord( vElf1[i] ) - ord('a') + 1 ; 
              if vElf1[i].isupper(): vCurrent = vCurrent + ord( vElf1[i] ) - ord('A') + 27; 

            k=k+1
        j=j+1
      i=i+1

print(vCurrent);
vfFile.close()