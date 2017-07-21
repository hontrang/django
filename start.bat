:: This script to bootup django web backend
TITLE This script to bootup django web backend
@echo off

:: CONFIGURATIONS

SET ENV_ACTIVE_SCRIPT=env\scripts\activate
SET SLEEP_TIME=2
SET ROOT=backend

:: MAIN SCRIPT
CALL %ENV_ACTIVE_SCRIPT%
TIMEOUT %SLEEP_TIME%
CD %ROOT%
REM ECHO %CD%
python manage.py runserver
PAUSE


