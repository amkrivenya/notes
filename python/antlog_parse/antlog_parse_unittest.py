#!/usr/bin/python

###   Comment: Parsing ant log of ABL Unittest
###   Run by:  NOT YET gitlab-runner
###   Used by: NOT YET pipeline on the test stage (.gitlab-ci.yml), after compile
###   Author:  krivenya_a

import os

vTST_RSLT = os.getenv('TST_RSLT') 
vPRD_NM = os.getenv('PRD_NM')
vPRD_TST = os.getenv('PRD_TST')
vTST_NOTIFY = os.getenv('TST_NOTIFY')

vAnt_log_file = vTST_RSLT + '/ant/' + vPRD_NM + '.' + vPRD_TST +'.ant_utst.log'
vfLogfile = open(vAnt_log_file, mode="r")

vError_ErrorsFailures = False
vError_Failure_to_invoke = False
vError_BUILD_FAILED = False

for line in vfLogfile:

    ### Error type: "... Errors: XXX, Failures: XXX ... "
    # Middle section of forming vOS
    # "Middle" if-section goes first because we start to process from second line of logs block (not to do first(previous) line twice)
    if vError_ErrorsFailures and len(line) > 1 and line.find("[ablunit] Running") < 0:
        vOS = vOS + line
    # Entry section of forming vOS
    if "Errors" in line:
        # Find out number of Failures, if more than zero - switch on Boolean variable
        i1 = line.find("Failures: ")
        i = int(line[i1+10:i1+11])
        if i > 0: vError_ErrorsFailures = True
        # Find out number of Errors, if more than zero - switch on Boolean variable
        i1 = line.find("Errors: ")
        i = int(line[i1+8:i1+9])
        if i > 0: vError_ErrorsFailures = True
        # Start forming vOS with ECHO, ant logfile name, previous and current line
        vOS = 'echo -e "' + vAnt_log_file + '\x0A\x0A'
        vOS = vOS + vPrevious_line + line
    # Final section of forming vOS
    if vError_ErrorsFailures and ( len(line) == 1 or line.find("[ablunit] Running") > 0 ):
        # Finish forming vOS with MAILX and send it to OS to execute, switch off Boolean variable
        vOS = vOS + '" | mailx -r "ABL_Unittest" -s "ABL Unittest Notification. PROJECT: ' + vPRD_NM + ' SUITE: ' + vPRD_TST + '" ' + str(vTST_NOTIFY)
        os.system(vOS)
        vError_ErrorsFailures = False

    ### Error type: "Failure to invoke ABLUnit runtime"
    # Middle section of forming vOS
    # "Middle" if-section goes first because we start to process from second line of logs block (not to do first(previous) line twice)
    if vError_Failure_to_invoke and len(line) > 1:
        vOS = vOS + line
    # Entry section of forming vOS
    if "Failure to invoke ABLUnit runtime" in line:
        vError_Failure_to_invoke = True
        vOS = 'echo -e "' + vAnt_log_file + '\x0A\x0A'
        vOS = vOS + vPrevious_line + line
    # Final section of forming vOS
    if vError_Failure_to_invoke and len(line) == 1:
        vOS = vOS + '" | mailx -r "ABL_Unittest" -s "ABL Unittest Notification. PROJECT: ' + vPRD_NM + ' SUITE: ' + vPRD_TST + '" ' + str(vTST_NOTIFY)
        os.system(vOS)
        vError_Failure_to_invoke = False

    ### Error type: "BUILD FAILED"
    # Entry section of forming vOS
    if "BUILD FAILED" in line:
        vError_BUILD_FAILED = True
        vOS = 'echo -e "' + vAnt_log_file + '\x0A\x0A'
    # Middle section of forming vOS
    if vError_BUILD_FAILED and len(line) > 1:
        vOS = vOS + line
    # Final section of forming vOS
    if vError_BUILD_FAILED and len(line) == 1:
        vOS = vOS + '" | mailx -r "ABL_Unittest" -s "ABL Unittest Notification. PROJECT: ' + vPRD_NM + ' SUITE: ' + vPRD_TST + '" ' + str(vTST_NOTIFY)
        os.system(vOS)
        vError_BUILD_FAILED = False

    # Save previous line to process it for some type of errors
    vPrevious_line = line

# Close ant logfile
vfLogfile.close()



# Tmp Block for processing ABLUnit report file
# if os.path.isfile(vTST_RSLT + "/" + vPRD_NM + "/Test-ABLUnit-ptest_" + vPRD_TST+ ".xml"):
# else:
#     vOS = 'echo -e "BODY. See catalog ' + vTST_RSLT + '" | mailx -r "pipeline" -s "ABL Unittest ' + vPRD_NM + ' did not start" krivenya_a@exon-it.by'  
#     os.system(vOS)

