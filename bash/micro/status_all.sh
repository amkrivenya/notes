#!/bin/bash

WD='/srv/micro'
iproc=0
iserv=0

for SERVICE in \
crm-gateway-pg \
crm-client-pg \
crm-db-adapter-pg \
crm-db-notice-handler-pg \
crm-dim-pg \
crm-loan-conveyor-pg \
crm-reporting-pg \
crm-storage-pg \
crm-todo-task-manager-pg \
oauth2sv-pg
do

  PGREP_RETURN=$(pgrep -u micro -a | grep $SERVICE | awk '{print $1, $4}')

  if [[ $PGREP_RETURN == *$WD/$SERVICE* ]];
  then

    echo -ne "\e[32mProcess $SERVICE exists:\e[0m" $PGREP_RETURN "\n"
    iproc=$(($iproc+1))

    line=$(cat $WD/$SERVICE/log/$SERVICE.log | grep 'JVM running for' | cut -f9- -d ' ')
    if [[ ! -z $line ]];
    then
      echo -e "\e[32mService $SERVICE was started:\e[0m" $(cat $WD/$SERVICE/log/$SERVICE.log | grep 'JVM running for' | cut -f9- -d ' ')
      iserv=$(($iserv+1))
    else
      echo line: $line
      echo -ne "\e[31m Service $SERVICE was not started (Start record does not exist in the current log).\e[0m\n"
    fi

  else
    echo -ne "\e[31mProcess $SERVICE does not exist.\e[0m\n"
  fi
  echo -e 
done

echo -e "Running \e[32m$iproc\e[0m processes."
echo -e "Started \e[32m$iserv\e[0m services (Start records are exist in the current log)."
echo -e "---------------------"
