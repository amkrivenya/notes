#!/usr/bin/python
import os

vcFile='04_in.txt'
vfFile = open(vcFile, mode="r")

vCurrent=0

for line in vfFile:
  line = line.replace('\r', '')  
  i = line.find("-")
  vElf1 = int( line[0:i] )

  j = line.find(",")
  vElf2 = int( line[i+1:j] )

  i = line.rfind("-")
  vElf3 = int ( line[j+1:i] )
  vElf4 = int ( line[i+1:len(line)-1] )

  if ( vElf1 < vElf3 ):
    if ( vElf3 <= vElf2 ): vCurrent = vCurrent + 1
  else: 
    if( vElf1 > vElf3 ):
      if ( vElf4 >= vElf1 ): vCurrent = vCurrent + 1
    else:  vCurrent = vCurrent + 1

print(vCurrent);
vfFile.close()