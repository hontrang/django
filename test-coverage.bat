:: This script to bootup django web backend
:: Code coverage describes how much source code has been tested. 
:: It shows which parts of your code are being exercised by tests and which are not. 
:: It’s an important part of testing applications, so it’s strongly recommended to check the coverage of your tests.
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
:: execute to collect data
coverage run --source='.' manage.py test webapp
:: show data as report
coverage report

CD ..
PAUSE


