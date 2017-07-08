@echo off
title SETUP MONGODB AS SERVICE
echo PLEASE RUN WITH ADMINISTRATOR
mkdir D:\MongoDB\data
echo ##### Created data path #####
mkdir D:\MongoDB\log
copy /b NUL D:\MongoDB\log\log_mongodb.log
echo ##### Created log path #####
cd C:\Program Files\MongoDB\Server\3.4\bin
echo ##### Open root directory MongoDB to perform mongod #####
mongod --directoryperdb --dbpath D:\MongoDB\data --logpath D:\MongoDB\log\log_mongodb.log --logappend --rest --install
echo ##### Start service MongoDB #####
net start MongoDB
echo ############### DONE ################