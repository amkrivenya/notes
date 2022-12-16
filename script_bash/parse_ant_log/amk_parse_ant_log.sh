#!/bin/bash

###   Comment: Parsing ant log, not used now, replaced by python script /opt/bqbuild/amk_py/amk_parse_ant_log.py
###   Run by:  gitlab-runner
###   Used by: pipeline on the test stage (.gitlab-ci.yml), after compile
###   Author:  krivenya_a

# Define source logfile name and workdir
workdir=/opt/bqbuild/amk
ant_log_file='/home/gitlab-runner/builds/-gTWTeBL/0/buzhan_d/bq_build/ant_bqn.log'
#ant_log_file='/opt/bqbuild_amk/log/ant_bqn.log'

# Username/password for SVN repo
USER=sync
PASS=*******

# Remove previous files
#rm -f $workdir/amk_error_files_list_previous.txt
rm -f $workdir/tmp*.txt

# Rename the last filelist to new file for save it to compare new filenames with it, if the last filelist is not exist - create empty
# -f return if file exist (-s is it empty, -d is directory exist)
if [ -f "$workdir/amk_error_files_list.txt" ]
then
  mv $workdir/amk_error_files_list.txt $workdir/amk_error_files_list_previous.txt
else
  touch $workdir/amk_error_files_list_previous.txt
fi

# Start value of errors - in current version counter is using only for debug
i=0

# Extract filenames from source logfile by grepping line ( grep - select lines matching "Error compiling", awk - select filename from string from fifth column)
for line in `cat $ant_log_file | grep "Error compiling" | awk '{print $5}'`
do

  # increase counter of errors
  let "i += 1"

  # Variable $line in the cycle will contain path and filename of error files from ant log in `apostrophes`!

  # Get clear full path and filename - delete apostrophes from begin and end of $line
  file=$(echo $line | awk '{gsub("'\''","")}1')

  # Get from svn author of last commit ( grep r - grep lines with revision number (for ex. "r12424", grep m1 - grep only first match (revision number is a first info)
  author=$(svn log -l1 --username $USER --password $PASS $file | grep r -m1 | awk '{print $3}')

  # For some incorrect svn usernames correcting adresses
  exist=0
  if [ $author = 'anaschenko' ]; then mail='anaschenko_s@exon-it.by'; exist=1; fi
  if [ $author = 'kalinovs' ];   then mail='kalinovsky_a@exon-it.by'; exist=1; fi
  if [ $author = 'svekshin' ];   then mail='vekshin_s@exon-it.by';    exist=1; fi
  if [ $author = 'iantonov' ];    then mail='krivenya_a@exon-it.by';  exist=1; fi
  if [ $author = 'popov_v' ];    then mail='krivenya_a@exon-it.by';   exist=1; fi
  if [ $exist = "0" ]; then mail=$author'@exon-it.by'; fi

      #### Temporary output for debug
      # echo $mail >> $workdir/tmp_adressbook.txt

  # Section if will need exclude somebody
  if true
  #[ $author != 'kalinovs' ] && [ $author != 'popov_v' ] && [ $author != 'ban_m' ] && [ $author != 'svekshin' ] && [ $author != 'kravchenko_i' ]
  then

    # get info of last commit and remove all markdown symbols '-' from it
    svn=$(echo $(svn log -l1 --username $USER --password $PASS $file) | awk '{gsub("'\-'","")}1')

    # add filename without path and error text to summary variable $text 
    text=$text$(basename $file)'\x0ALast commit of this file was:'$svn'\x0A\x0A'

    # Write filename to file - next time it will be compared with it
    echo $(basename $file) >> $workdir/amk_error_files_list.txt

    # Search filename in previous filelist
    exist=0
    while read proc
    do
      # Check, if the current file is equal to one of lines from previous file
      if [ "$(basename $file)" = "$proc" ]; then exist=1; fi
    done < $workdir/amk_error_files_list_previous.txt

        #### Temporary output for debug
        # echo -e $exist > $workdir/tmp_exist_$i.txt

    # If file not match to any lines from previous list - then it is new 
    if [ $exist = "0" ]
    then

      # Send mail to author
      echo -e 'Error compiling file: '$(basename $file)'\x0A\x0ALast commit at SVN repository was: '$svn | mailx -r "pipeline" -s 'Error compiling file: '$(basename $file) $mail
      echo -e 'Error compiling file: '$(basename $file)'\x0A\x0ALast commit at SVN repository was: '$svn'\x0A\x0AMail sent to: '$mail | mailx -r "pipeline" -s 'Error compiling file: '$(basename $file) krivenya_a@exon-it.by,buzhan_d@exon-it.by

      # Add new file to summary variable $new, for show all new files in summary email subject
      new=$new$(basename $file)','

        #### Temporary output for debug
        # echo -e 'Text: '$svn'\x0A\x0A Subject: New file: '$(basename $file)'\x0A\x0A Address: '$mail > $workdir/tmp_maillists_$i.txt
    fi
  fi
done

        #### Temporary output for debug
        # echo -e $text > $workdir/tmp_mail_text.txt

# For del
# Read previous value of errors or set var to 0 if file is not exist
#if [ -f "$workdir/amk_count.txt" ] 
#then
#  i_last=$(cat $workdir/amk_count.txt)
#else 
#  i_last=0
#fi
# If current number of errors is not equal to previous valus then send mail
#if true
#if [ "$i" -ne "$i_last" ]
# Save current number of error files for nest check
#echo $i > $workdir/amk_count.txt


# If variable $new is not empty - send summary email
if [ $(echo $new | awk '{print length}') -gt 1 ]
then
 
  # send mail by mailx
   echo -e $text | mailx -r "pipeline" -s 'Errors in pipeline: '$i', new files: '$new krivenya_a@exon-it.by,buzhan_d@exon-it.by

        #### Temporary output for debug
        #  echo -e $text > $workdir/tmp_mail_text.txt
fi

rm -f $workdir/amk_error_files_list_previous.txt
