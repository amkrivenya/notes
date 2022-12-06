#!/usr/bin/python

###   Comment: Parsing ant log
###   Run by:  gitlab-runner
###   Used by: pipeline on the test stage (.gitlab-ci.yml), after compile
###   Author:  krivenya_a

import os

# Constantes              
vcAnt_log_file='/home/gitlab-runner/builds/-gTWTeBL/0/buzhan_d/bq_build/ant_bqn.log'
vcOutfile='/opt/bqbuild/amk_py/errors.txt'

vcUSER='sync'
vcPASS='*********'

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
vFirst = True
i=0

# Cycle processing log file by lines and preparing blocks of separated error between lines with text "Error compiling file" 
for line in vfLogfile:

    if "Error compiling" in line:

        ## As it is not possible to define is it the last error - boolean variable vFirst used for define "is it first"

        # If it is the first error - do nothing - just ordinary action - preparing variables 
        # If it is not the first error - then sending email using collected variables (vError, vFileName, vSVN) 
        if not vFirst and vNewError:
            # Forming command line for OS
            vOS = 'echo -e "Error compiling file:\x0A\x0A' + vFileName 
            vOS = vOS + '\x0A\x0A\x0ALast commit at SVN repository was: \x0A\x0A' + vSVN 
            vOS = vOS + '\x0A\x0AError: \x0A\x0A' + vError 
#            vOS = vOS + '\x0A\x0AMailto: \x0A\x0A' + vAuthor 
#            vAuthor='krivenya_a@exon-it.by' 
            vOS = vOS + '" | mailx -r "pipeline" -s "Error compiling file: ' + vFileName + '" krivenya_a@exon-it.by,' + vAuthor
            #print(vOS)
            #print('if not vFirst: --- send email ---',vFileName)
            os.system(vOS)

        ## This point is start of processing certain error
        # Clear variables after sending email, preparing for the next error
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

        # For some incorrect SVN usernames correcting adresses
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
        if vAuthor=='iantonov':
            vAuthor='krivenya_a@exon-it.by' 
            exist=1
        if vAuthor=='popov_v':
            vAuthor='krivenya_a@exon-it.by' 
            exist=1
        if exist==0 :
            vAuthor = vAuthor + '@exon-it.by'
            exist=1

    # Ordinary action in cycle if line does not containg "Error compiling file"  
    vError = vError + line
    #    print(line)

# After cycle, vError contain text from begining last errortext and up to end of log file - need to cut unuseful text
# Define end position of last errortext by searching double CR which means end of last error block
i1 = vError.find("\n\n")
vErrorLast = vError[0:i1]

# Sending mail with last error by OS echo/mailx
if vNewError:
    vOS = 'echo -e "Error compiling file:\x0A\x0A' + vFileName 
    vOS = vOS + '\x0A\x0A\x0ALast commit at SVN repository was: \x0A\x0A' + vSVN
    vOS = vOS + '\x0A\x0AError: \x0A\x0A' + vErrorLast 
#    vOS = vOS + '\x0A\x0AMailto: \x0A\x0A' + vAuthor 
#    vAuthor='krivenya_a@exon-it.by' 
    vOS = vOS + '" | mailx -r "pipeline" -s "Error compiling file: ' + vFileName + '" krivenya_a@exon-it.by,' + vAuthor
    os.system(vOS)
    #print(vOS)

vfLogfile.close()
vfOutfile.close()
vfPrevFile.close()
try: os.remove(vcOutfile+'_old')
except: pass

