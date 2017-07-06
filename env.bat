:: This script to setup env
TITLE This script to setup env
@eho off

:: CONFIGURATIONS

SET ENV_ACTIVE_SCRIPT=env\scripts\activate
SET SLEEP_TIME=2
SET ROOT=backend

:: MAIN SCRIPT
pip install virtualenv
pip install virtualenvwrapper-win
virtualenv env
call %ENV_ACTIVE_SCRIPT%
TIMEOUT %SLEEP_TIME%
pip install Django
pip install mongoengine
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
pip install django-rest-framework-mongoengine
pip install django-rest-swagger
pip install django-cors-headers
pip install pillow
pip install pytest

CD %ROOT%
ECHO %CD%
python manage.py runserver
PAUSE


