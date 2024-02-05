#!/bin/bash

# When you run script with absolute path from random location
# pwd command inside script will return path to your current location,
# but not to the dir of the running script 
# 
# So do not use in the scripts: ROOT=$(pwd)
#
# Use this:

ROOT=`cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd`   

echo $ROOT

# Explanation:

echo 1: ${BASH_SOURCE[0]}   : get absolute path to executed script 

echo 2: $( dirname -- "${BASH_SOURCE[0]}" )  : get its dirname path

echo 3: `cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd` : change directory to received value and if it was successful - return value of pwd command


# https://www.gnu.org/savannah-checkouts/gnu/bash/manual/bash.html#Lists
#
# command1 & command2
# If a command is terminated by the control operator ‘&’, the shell executes the command asynchronously in a subshell.
# This is known as executing the command in the background, and these are referred to as asynchronous commands.
# The shell does not wait for the command to finish, and the return status is 0 (true). 

# command1 && command2
# command2 is executed if, and only if, command1 returns an exit status of zero (success). 

# "--" https://habr.com/ru/articles/47706/


