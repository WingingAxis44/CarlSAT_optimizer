#!/bin/bash

#Automatically adds all relevant files+folders for staging.
#Remember to commit after!

#This script also performs a database dump. The name of the container (i.e. mysql-db) shouldn't change.
#Note: The hyperopt database will be dumped into two places. Namely sclscripts and dbBackups. 
#Both sclscripts and dbBackups are in our git repo.
#sclscripts has the file <hyperopt.sql> which is our "most-up-to-date" hyperopt DB.
#dbBackups stores all the incremental backups made. This allows for us to have a contingency plan incase
#anything goes wrong and we need to restore our database from an older, healthy version.

#The following dumps hyperopt db stored on your local volume into shared folder (accessed from git repo).
# i.e. This overwrites sqlscripts/hyperopt.sql with your local version of the hyperopt db.

echo -e "\e[1;36mDump local hyperopt database to sqlscripts/hyperopt.sql\e[0m"

sudo docker exec mysql-db sh -c 'exec mysqldump hyperopt -uroot -ppw' >./sqlscripts/hyperopt.sql

#sqlscripts folder is staged
#git add sqlscripts/

#The following creates an incremental backup of hyperopt db. dbBackup is also shared through our git repo.
#No overwriting is done, as each backup is unique.

NOW=$(date +"%m-%b-%Y_%H-%M-%S")
echo -e "\e[1;36mBacked up hyperopt database to dbBackups, filename = backup_${NOW}\e[0m"

sudo docker exec mysql-db sh -c 'exec mysqldump hyperopt -uroot -ppw' >./dbBackups/backup_$NOW.sql 

#Backups are staged
#git add dbBackups/


#Source file staging
#git add src/

#Miscellaneous
#git add autorun.sh
#git add windows_autorun.bat
#git add gitAuto.sh
#git add Dockerfile
#git add README.md
#git add wcards/

echo -e "\e[1;36mStaging complete. Remember to commit now!\n"