#!/bin/bash

ROOT=/data1
URL="https://***/wshtm/cgi-bin/conv.wsc/conv.p"

if ! [ -d $ROOT/_in ]; then mkdir -p $ROOT/_in; fi;
if ! [ -d $ROOT/_in_processed ]; then mkdir -p $ROOT/_in_processed; fi;
if ! [ -d $ROOT/_in_rejected ]; then mkdir -p $ROOT/_in_rejected; fi;
if ! [ -d $ROOT/_out ]; then mkdir -p $ROOT/_out; fi;
if ! [ -d $ROOT/log ]; then mkdir -p $ROOT/log; fi;
if ! [ -d $ROOT/tmp ]; then mkdir -p $ROOT/tmp; fi;

if [ $(find $ROOT/_in -maxdepth 1 -type f | wc -l) -eq 0 ]
then
  exit
fi

if [ -z "$ERRORS" ]; then ERRORS="12"; fi;
if [ -z "$WAIT" ]; then WAIT="60"; fi;
if [ -z "$SLEEP" ]; then SLEEP="3600"; fi;

TMP0=$ROOT/tmp/curl.html
TMP1=$ROOT/tmp/out.tmp1
TMP2=$ROOT/tmp/out.tmp2

LOG=$ROOT/log/conv.log
LOGDEBUG=$ROOT/log/log-debug.log

echo -e "\n" $(date) >> $LOG
echo -e "\n"

cout_err=0

for FILE in `find $ROOT/_in -maxdepth 1 -type f | sort`
do

  echo -n $FILE "  zipped, uploading...  " 
  echo -n $FILE "  zipped, uploading...  " >> $LOG

  /data2/zip -j -q $FILE.zip $FILE >> $LOGDEBUG

  echo curl -v --insecure --max-time $WAIT -F "filename=@$FILE.zip" -X POST $URL >> $LOGDEBUG
  /data2/curl -v --insecure --max-time $WAIT -F "filename=@$FILE.zip" -X POST $URL >$TMP0 2>>$LOGDEBUG

  echo -n " downloading...  "
  echo -n " downloading...  " >> $LOG

  /data2/strings $TMP0 > $TMP1

  ERR36=$(cat $TMP1 | grep ': 36')

  cat $TMP1 | grep logs > $TMP2
  /data2/sed -e 's/.*href=//' $TMP2 > $TMP1
  /data2/sed -e 's/>.*//' $TMP1 > $TMP2
  rm -rf $TMP1

  if [ ${#ERR36} -ne 0 ]
  then
    rm -rf $FILE.zip
    echo "Waiting time is 36 sec, exit."
    echo "Waiting time is 36 sec, exit." >> $LOG 
    echo ">> Timeout 36 sec means that QBIS converter is not working now, slepping for $SLEEP seconds before next try..." 
    echo ">> Timeout 36 sec means that QBIS converter is not working now, slepping for $SLEEP seconds before next try..." >> $LOG 
    sleep $SLEEP
    exit;
  fi

  if [ ${#TMP2} -ne 0 ]
  then
    /data2/wget --no-check-certificate $(cat $TMP2) -P $ROOT/_out >> $LOG 2>> $LOGDEBUG
  fi

  CONVNAME=$ROOT/_out/$(basename $FILE)
  if [ -f $CONVNAME.zip ];
  then 
    echo " converted, moving to processed, OK!"
    echo " converted, moving to processed, OK!" >> $LOG
    mv $FILE $ROOT/_in_processed;
    cout_err=0
    chmod 777 $CONVNAME.zip
  else 
    echo " was not converted for $WAIT sec, moving to rejected, ERROR..."
    echo " was not converted for $WAIT sec, moving to rejected, ERROR..." >> $LOG
    mv $FILE $ROOT/_in_rejected;
    let "cout_err += 1"
  fi

  rm -rf $FILE.zip

  if [ $cout_err = $ERRORS ] 
  then
    echo "Number of errors reached the limit: "$ERRORS
    echo "Number of errors reached the limit: "$ERRORS >> $LOG 
    exit;
  fi

done

#mv $ROOT/_rejected/* $ROOT/_in/
#echo "moving all rejected filer to /"_in/" folder" 
#echo "moving all rejected filer to /"_in/" folder" >> $LOG

echo "The \"_in\" folder is empty, finished!" 
echo "The \"_in\" folder is empty, finished!" >> $LOG
echo $(date) >> $LOG
