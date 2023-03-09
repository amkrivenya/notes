#!/usr/bin/python
import os
import time

def srch(data):
  vFlag = 0
  for i in range (len(data)):
    for j in range (i+1,len(data)):
     if data[i] == data[j]: 
       vFlag = 1;
  return vFlag

vSize = 14

#code = ["","","","","","","","","","","","","","",]
code = [""] * vSize

vcFile='06_in.txt'
vfFile = open(vcFile, mode="r")

vPos = vSize
for i in range(vSize): code[i] = vfFile.read(1)

while srch(code):
  for i in range(vSize-1): code [i] = code [i+1]
  code [vSize - 1] = vfFile.read(1)
  vPos = vPos + 1

print(code, vPos)

vfFile.close()

