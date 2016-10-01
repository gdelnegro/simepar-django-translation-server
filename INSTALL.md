# Dependencies
PostgreSQL 9.5.x (https://www.postgresql.org/docs/9.5/static/tutorial-install.html)

PostGIS 2.2.1 (http://postgis.net/install/)

Python 3 (https://www.python.org/)

Python Virtualenv (https://virtualenv.pypa.io/en/stable/installation/)

Python pip (https://pip.pypa.io/en/stable/installing/)

Libjpeg (http://libjpeg.sourceforge.net/)

Apache2 (https://httpd.apache.org)

Apache 2 mod_wsgi

DjangoRestFramework

Django Model Translation

##Project installation

###Installing dependencies
Below, are listed a couple of examples of how to install the dependencies for Debian/Ubuntu systems, and CentOS/RedHat.

#### Debian/Ubuntu
With superuser privileges, execute the following commands:
```bash
apt-get install postgresql-server-dev-all # install postgreSQL
apt-get install postgis # install postGIS extension for postgreSQL
apt-get install libjpeg-dev # install libjpeg extension
apt-get install python3-dev # install python3 header files and static library for Python 3
apt-get install python3-pip
pip install --upgrade virtualenv # install or upgrade virtualenv
```

#### CentOS/RedHat
First make sure we are running latest version of virtualenv. There is a bug in the version provided by the yum package, check: https://gitlab.com/mailman/mailman-bundler/issues/19
With superuser privileges, execute the following commands:

```bash
pip install --upgrade virtualenv
```

Install yum development packages dependencies:

```bash
yum install libjpeg-turbo-devel # install libjpeg extension
yum install zlib-devel # install zlib compression library
yum install python34-devel # install python3 header files and static library
yum install postgresql-devel # install postgresql

```

### Database Configuration

The CDMS Metadata relies on a PostgreSQL database with PostGIS extension. The database can be created with the following commands:

With superuser permissions, login as postgres user:
```bash
sudo -su postgres
```
As postgres user, connect to postgreSQL `psql`, and execute the following commands:

Wallops
```bash
CREATE ROLE simepar_translation WITH LOGIN; # create the user simepar_translation
CREATE DATABASE simepar_translation WITH OWNER simepar_translation; # create the database simepar_translation, with user simepar_translation as owner
ALTER ROLE simepar_translation WITH PASSWORD 'simepar_translation'; # alter user simepar_translation password.
ALTER ROLE simepar_translation SET CLIENT_ENCODING = 'utf8'; # set user cdms_wallops default connection encoding to UTF-8
ALTER ROLE simepar_translation SET default_transaction_isolation TO 'read committed'; # set user cdms_wallops default transaction isolation
ALTER ROLE simepar_translation SET timezone TO 'UTC'; # set user simepar_translation timezone to UTC

```

If you changed your database credentials, please update the files  `src/simepar-django-translation-server/settings/development.py` for development settings and `src/simepar-django-translation-server/settings/production.py` for production 

###Preparing the Virtualenv

You must first create your virtualenv with python3. For this, execute the following commands on the root directory of your project location:
 
 ```bash
virtualenv -p python3 env # install a python virtualven on the 'env' directory with python 3
source env/bin/activate # activate your virtualenv
pip install -r requirements.txt # install all the packages listed on the requirements.txt file, with it's specified versions
 ```

###Installing the project

First of all, activate your virtualenv with `source env/bin/activate`, then execute the following commands on the root directory of your project location:

Please, replace ENVIRONMENT with the environment you are deploying (development or production)

```bash
python src/manage.py makemigrations --settings=django_simepar_translation_server.settings.ENVIRONMENT # create any pending migrations for the project
python src/manage.py migrate --settings=django_simepar_translation_server.settings.ENVIRONMENT # apply the database changes to PostgreSQL
python src/manage.py collectstatic --settings=django_simepar_translation_server.settings.ENVIRONMENT # collect all static files for deployment
```

###Deploying the project

####Apache2 wsgi configuration
Django basic wsgi deploy directives:
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/modwsgi/

Replace `YOUR_PROJECT_PATH` with your project path

Basic apache configuration:
```
WSGIDaemonProcess cdms-wallops python-path=YOUR_PROJECT_PATH/src:YOUR_PROJECT_PATH/env/lib/python3.4/site-packages
WSGIScriptAlias /cdms/wallops YOUR_PROJECT_PATH/src/cdms/wsgi-wallops-production.py

RedirectMatch "/cdms/wallops$" "/cdms/wallops/"
<Location "/cdms/wallops/" >
    WSGIProcessGroup cdms-wallops
</Location>

<Directory YOUR_PROJECT_PATH/src/cdms/>
    <Files wsgi-wallops-production.py>
        Require all granted
    </Files>
</Directory>

Alias "/cdms/wallops/static" "YOUR_PROJECT_PATH/src/static"
<Directory "YOUR_PROJECT_PATH/src/static/">
    Require all granted
</Directory>
```

####For testing purposes
Activate your virtualenv with `source env/bin/activate`, then execute the following command on the root directory of your project location:
```bash
python src/manage.py runserver --settings=django_simepar_translation_server.settings.ENVIRONMENT 127.0.0.0:8000
```
