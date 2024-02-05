#!/bin/bash

# Set your globals before:
# git config --global user.email "krivenya_a@exon-it.by"
# git config --global user.name "Aleksey Krivenya"
#
# For ssh - add your key to gitlab profile 

echo -e '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n'
echo -e '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n\n'

ROOT=`cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd`   

PRJ_LIST="$ROOT/prj_list"                      # Define the list of the projects to join into the target project
export ROOT PRJ_LIST

`sed -i "s/\r//g" $PRJ_LIST`                   # If exist - remove ^M (/r) from file $PRJ_LIST

SOURCE_GIT="gitlab.local.exon-it.by:3022"      # Define source URL
SOURCE_GROUP="exon-internal/sonic"             # Define the group of the projects from 

TARGET_GIT="192.168.29.46:3022"                # Here place URL to the new git
TARGET_PROJECT="for_del"                       # Here place the name of new project
TARGET_GROUP="group1"                          # Here place its group

export SOURCE_GIT SOURCE_GROUP TARGET_GIT TARGET_GROUP TARGET_PROJECT

cd $ROOT
git clone ssh://git@$TARGET_GIT/$TARGET_GROUP/$TARGET_PROJECT.git

while read line
do

echo -e '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n\n'

  PRJ=`echo $line | awk '{print $1}'`

  if [ $(echo $PRJ | awk '{print length}') -gt 0 ] && [ ${PRJ:0:1} != '#' ] 
  then

    export PRJ
#    # Second parameter - reserved (left over from another template)
#    PAR2=`echo $line | awk '{print $2}'`
#    export PAR2

    cd $ROOT

    echo -e '-------------------------------------------------------------------------------\n'
    echo ">>>>>>> git clone ssh://git@$SOURCE_GIT/$SOURCE_GROUP/$PRJ.git"

    git clone ssh://git@$SOURCE_GIT/$SOURCE_GROUP/$PRJ.git

    mkdir $ROOT/$PRJ/$PRJ

    echo ">>>>>>> mv $ROOT/$PRJ/* $ROOT/$PRJ/$PRJ"
    mv $ROOT/$PRJ/* $ROOT/$PRJ/$PRJ


    find $ROOT/$PRJ/ -name ".*" -type f -exec sh -c 'mv "$@" $ROOT/$PRJ/$PRJ/' _ {} \;

    echo ">>>>>>> cd $ROOT/$PRJ"
    cd $ROOT/$PRJ

    echo ">>>>>>> git add ."
    git add .

    echo ">>>>>>> git commit -m "Main branch of separate project $PRJ from group $SOURCE_GROUP was merged as a folder to this general project""
    git commit -m "Main branch of separate project $PRJ from group $SOURCE_GROUP was merged as a folder to this general project"

    echo ">>>>>>> cd $ROOT/$TARGET_PROJECT"
    cd $ROOT/$TARGET_PROJECT

    echo ">>>>>>> git remote add $PRJ $ROOT/$PRJ "
    git remote add $PRJ $ROOT/$PRJ 

    echo ">>>>>>> git fetch $PRJ"
    git fetch $PRJ

    echo -e $PRJ\n
    if [$PRJ == 'omen-udf-store-service']
    then read -p "Press any key to continue... " -n1 -s
    fi


    echo ">>>>>>> git merge $PRJ/master --allow-unrelated-histories"
    git merge $PRJ/master --allow-unrelated-histories

#    git merge $PRJ/main --allow-unrelated-histories
#    git merge $PRJ/development --allow-unrelated-histories
#    git merge $PRJ/exon --allow-unrelated-histories
#    git merge $PRJ/redmine-2.1 --allow-unrelated-histories

  fi
done < $PRJ_LIST

echo -e '-------------------------------------------------------------------------------\n'
echo
echo "Check the output of the script and run:"
echo
echo "cd $ROOT/$TARGET_PROJECT"
echo "git push origin"
echo
