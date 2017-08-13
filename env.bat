:: This script to setup env
TITLE This script to setup env
@eho off

:: CONFIGURATIONS

SET ENV_ACTIVE_SCRIPT=env\scripts\activate
SET SLEEP_TIME=5
SET ROOT=backend

:: MAIN SCRIPT
pip install virtualenv
pip install virtualenvwrapper-win
virtualenv env

REM COMMENT OUT CODE TO INSTALL PACKAGE GLOBALLY
CALL %ENV_ACTIVE_SCRIPT%
TIMEOUT %SLEEP_TIME%
REM COMMENT OUT CODE TO INSTALL PACKAGE GLOBALLY

pip install Django
pip install mongoengine
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
pip install django-rest-framework-mongoengine
pip install django-rest-swagger
pip install django-cors-headers
pip install pillow
pip install -U pytest
pip install pytest-django
pip install pytest-cov
pip install coverage
pip install psycopg2

CD %ROOT%
ECHO %CD%
python manage.py runserver
PAUSE


