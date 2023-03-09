#!/usr/bin/python
import os
from datetime import datetime

print(datetime.now())

# Procedure read file by line until "$cd name"+"path=parent"
#   and then countsize until "cd another folder" found
def folder_scan(name, parent):

  vProcFile = open('07_in.txt', mode="r")
  vFldrSize=0
  vDone=0
  vOn=0
  path=''

  for line in vProcFile:
    line = line.replace('\r', '')  
    # If found command "cd target folder" - switch on counting
    if line.find('$ cd '+name) >= 0 and parent == path:
      vOn=1
      
    if line[0:4] == '$ cd': 
      # Set root path
      if line[5: len(line) - 1] == "/": path ="/"
      else:
        # Build path
        if line[5: len(line) - 1] == "..":
          path = path[: path.rfind("/")]
          if path == "": path ="/"
        else:
          if path == "/": path = path + line[5: len(line) - 1]  
          else: path = path + '/' + line[5: len(line) - 1]  

    # If found command "cd another folder" with switching on counting -
    #   that mean need to end counting and to end procedure
    if line.find('$ cd') >= 0 and line.find('$ cd '+name) < 0 and vOn == 1:
      vOn=0; vDone=1
  
  # If digits in line - add this number to counter of folder size
    if line[0] >= "0" and line[0] <= "9" and vOn:
      vFldrSize = vFldrSize + int( line[ : line.find(" ") ] )

    # If $dir with switching on counting - run recusively procedure and add result to counter of folder size
    if line[0:3] == 'dir' and vOn: 
      vFldrSize = vFldrSize + folder_scan(line[4: len(line) - 1], path)

    if vDone: break
  vProcFile.close()
  return vFldrSize

vfFile = open('07_in.txt', mode="r")
vfFileOut = open('07_out.txt', mode="w")

vFldrSize=0
vAll=0
path=''

for line in vfFile:
  line = line.replace('\r', '')  
  # If first digisymbolt in line digit - add whole number to counter of folder size
  if line[0] >= "0" and line[0] <= "9":
    vFldrSize = vFldrSize + int( line[ : line.find(" ") ])

  # If $dir - run procedure and add result to counter of folder size
  if line[0:3] == 'dir': 
    vFldrSize = vFldrSize + folder_scan(line[4: len(line) - 1], path)

  if line[0:4] == '$ cd': 
    # If $cd / - only set root directory
    if line[5: len(line) - 1] == "/": path ="/"; pathwrite='/'
    else:
      # If exit from folder - remove folder from path 
      if line[5: len(line) - 1] == "..":
        path = path[: path.rfind("/")]
        if path == "": path ="/"
      # Last variant (not /, not ..) - add folder name to path and clear counter of folder size
      else:
        if path == "/": path = path + line[5: len(line) - 1]  
        # Last else(not /, not ..) - add folder name to path 
        else: path = path + '/' + line[5: len(line) - 1]
        # Counter - count folders less than 100 000
        if vFldrSize < 100000:
          vAll = vAll + vFldrSize

        # Optional - write dirtree to the output file
        vfFileOut.write("%8d" % vFldrSize+' '+pathwrite+'\n')          
        pathwrite = path

        vFldrSize = 0

# Optional - write lasr folder to the output file
vfFileOut.write("%9d" % vFldrSize+' '+pathwrite+'\n')          

print (vAll);
vfFile.close()
vfFileOut.close()
print(datetime.now())
