#!/bin/bash

JDK_HOME='/srv/micro/java/jdk1.8.0_211'
JRE_HOME='/srv/micro/java/jre1.8.0_211'
JAVA_HOME=$JRE_HOME
JAVA=${JAVA_HOME}/bin/java
export JDK_HOME JRE_HOME JAVA_HOME JAVA

PATH=$PATH:$HOME/.local/bin:$HOME/bin:${JAVA_HOME}/bin
export PATH

wd='/srv/micro'
export wd

WD='/srv/micro'

# application.properties
for SERVICE in \
crm-client-pg \
crm-db-adapter-pg \
crm-db-notice-handler-pg \
crm-dim-pg \
crm-loan-conveyor-pg \
crm-reporting-pg \
crm-todo-task-manager-pg \
crm-storage-pg 
#crm-gateway-pg 
#oauth2sv-pg - yml
do
  psinfo=$(pgrep -f $SERVICE)
  if [ -z $psinfo ];
  then
    mv $WD/$SERVICE/log/$SERVICE.log $WD/$SERVICE/log/$SERVICE.log_prev
    cd $WD/$SERVICE
    $WD/scripts/service_management -user micro -name $SERVICE -prop 'application.properties' -base $WD -count 30 -kind start
    sleep 15
  else
    echo -ne "\n\e[34mProcess $SERVICE exists:\e[0m" - Action SKIPPED "\n"
  fi
done

# application.yml
for SERVICE in \
crm-gateway-pg \
oauth2sv-pg 
do
  psinfo=$(pgrep -f $SERVICE)
  if [ -z $psinfo ];
  then
    mv $WD/$SERVICE/log/$SERVICE.log $WD/$SERVICE/log/$SERVICE.log_prev
    cd $WD/$SERVICE
    $WD/scripts/service_management -user micro -name $SERVICE -prop 'application.yml' -base $WD -count 30 -kind start
    sleep 15
  else
    echo -ne "\n\e[34mProcess $SERVICE exists:\e[0m" - Action SKIPPED "\n"
  fi
done

echo -e 
echo -e ----------------------------------------------------------------------------------------------------
echo -e Status:
echo -e 

$WD/status_all.sh
