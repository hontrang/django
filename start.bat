:: This script to bootup django web backend
TITLE This script to bootup django web backend
@eho off

:: CONFIGURATIONS

SET ENV_ACTIVE_SCRIPT=env\scripts\activate
SET SLEEP_TIME=2
SET ROOT=backend

:: MAIN SCRIPT
REM CALL %ENV_ACTIVE_SCRIPT%
REM TIMEOUT %SLEEP_TIME%
CD %ROOT%
REM ECHO %CD%
python manage.py runserver
PAUSE


