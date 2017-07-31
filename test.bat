:: This script to bootup django web backend
TITLE This script to bootup django web backend
@eho off

:: CONFIGURATIONS

SET ENV_ACTIVE_SCRIPT=env\scripts\activate
SET SLEEP_TIME=2
SET ROOT=backend

:: MAIN SCRIPT
CALL %ENV_ACTIVE_SCRIPT%
TIMEOUT %SLEEP_TIME%
ECHO %DIR%
CD %ROOT%
REM python manage.py test webapp
pytest -v --junitxml=report.xml --html=report.html

CD ..
PAUSE


