#!/usr/bin/python

###   Comment: Parsing ant log which is the result of compiling bisquit src 
###   Run by:  gitlab-runner
###   Used by: pipeline on the test stage (.gitlab-ci.yml), after compile
###   Author:  krivenya_a

import os
import inspect

# Procedure for form vOS and send it by mailx
def senderror():
    # Forming command line for OS
    vOS = 'echo -e "Error of compiling file in the pipeline:\x0A\x0A' + vFileName 
    vOS = vOS + '\x0A\x0A\x0ALast commit at SVN repository was: \x0A\x0A' + vSVN 
    vOS = vOS + '\x0A\x0AError: \x0A\x0A' + vError 

#    vOS = vOS + '" | mailx -r "pipeline" -s "Error compiling file: ' + vFileName + '" ' + vDefault_recepients + ',' + vAuthor
### temporary added for certain file bqunittest.r - email it only for vDefault_recepients 
    if vError.find("bqunittest.r") > 0:
        vOS = vOS + '" | mailx -r "pipeline" -s "Error compiling file: ' + vFileName + '" ' + vDefault_recepients
    else:
        vOS = vOS + '" | mailx -r "pipeline" -s "Error compiling file: ' + vFileName + '" ' + vDefault_recepients + ',' + vAuthor

    os.system(vOS)


# Configuration parameterss
vcAnt_log_file='/home/gitlab-runner/builds/-gTWTeBL/0/buzhan_d/bq_build/ant_bqn.log'
vDefault_recepients='krivenya_a@exon-it.by,buzhan_d@exon-it.by'

# Creds for SVN
vcUSER=***
vcPASS=***

# Get current script's directory to save in it file errors.txt with previous errors
# https://stackoverflow.com/questions/3718657
filename=inspect.getframeinfo(inspect.currentframe()).filename
vcOutfile=os.path.dirname(os.path.abspath(filename)) + '/errors.txt'

# If exist file with previous errors then rename it to _old, else - create empty file to compare "with nothing"
if os.path.isfile(vcOutfile):
    os.rename(vcOutfile,vcOutfile+'_old')
else:
    vfOutfile = open(vcOutfile+'_old', mode="w")
    vfOutfile.close()

# Variables of files
vfLogfile = open(vcAnt_log_file, mode="r")
vfOutfile = open(vcOutfile, mode="w")

# Start values
vError = ''
i=0
# Flag for processing first error, cycle will define the end of the fist error by second "Error compiling"
vFirst = True
# Flag for processing last error, if it was the only one then mail will be send outside the main cycle
vNewError = False

# Main cycle for processing logfile line by line and preparing blocks of errors, separated by lines with "Error compiling file" 
for line in vfLogfile:

    if "Error compiling" in line:

        ## As it is not possible to define is it the last error - boolean variable vFirst used for define "is it first"

        # If it is the first error - do nothing - just ordinary action - preparing variables 
        # If it is not the first error - then sending email using collected variables (vError, vFileName, vSVN) 

        # If not the first erros - send mail and start to form next errorblock
        if not vFirst and vNewError:
            senderror()

        vFirst = False
        vNewError = True
        vError = ''

        # Extract absolute path for filename and SVN log
        i1 = line.find("'")
        i2 = line.rfind("'")
        vFilePath = line[i1+1:i2]

        # Extract filename (from end of absolute path to last "/")
        i1 = vFilePath.rfind("/")
        vFileName = vFilePath[i1+1:len(vFilePath)]

        # Save errorfiles to compare next time with them
        vfOutfile.write(vFileName+'\n');

        # Looking for the current error file in previous filelist
        vfPrevFile = open(vcOutfile+'_old', mode="r")
        for line2 in vfPrevFile:
            if line2.rstrip()==vFileName:
                vNewError = False
                #print(str(vNewError),vFileName)

        # Get SVN log info for last commit
        vSVN = os.popen('svn log -l1 --username ' + vcUSER + ' --password ' + vcPASS + ' ' + vFilePath).read()

        # Extract author from SVN log (between first and second "|")
        i1 = vSVN.find("|")
        vAuthor = vSVN[i1+2:len(vSVN)]
        i2 = vAuthor.find("|")
        vAuthor = vSVN[i1+2:i1+i2+1]

        # For some SVN usernames have to manualy define correct adresses
        exist=0
        if vAuthor=='anaschenko':
            vAuthor='anaschenko_s@exon-it.by'
            exist=1 
        if vAuthor=='kalinovs':
            vAuthor='kalinovsky_a@exon-it.by' 
            exist=1
        if vAuthor=='tsyganok':
            vAuthor='tsyganok_d@exon-it.by' 
            exist=1
        if vAuthor=='svekshin':
            vAuthor='vekshin_s@exon-it.by' 
            exist=1
        if vAuthor=='novicky_v':
            vAuthor='novickiy_v@exon-it.by' 
            exist=1
        if vAuthor=='iantonov':
            vAuthor=vDefault_recepients
            exist=1
        if vAuthor=='popov_v':
            vAuthor=vDefault_recepients
            exist=1
        if exist==0 :
            vAuthor = vAuthor + '@exon-it.by'
            exist=1

    # Ordinary action in cycle if line does not containg "Error compiling file" - adding such line to current errorblock
    vError = vError + line

# After cycle, vError contain text from the begining of last error and up to end of whole logfile - need to cut unuseful text
# Define end position of last errortext by searching double CR which means end of last error block
i1 = vError.find("\n\n")
vError = vError[0:i1]

# Sending mail with last error after cycle have finished
if vNewError :
    senderror()

# Closing all files
vfLogfile.close()
vfOutfile.close()
vfPrevFile = open(vcOutfile+'_old', mode="r")
vfPrevFile.close()
try: os.remove(vcOutfile+'_old')
except: pass
