# Collab Coursebook

![Django CI](https://github.com/DataManagementLab/collab-coursebook/workflows/Django%20CI/badge.svg)

## Description

Collab Coursebook is a plattform for collaborative learning und knowledge organization. It provides a place to share and re-use notes and other learning materials.

## Setup

This repository contains a Django project with several apps.


### Requirements

Collab Coursebook has two types of requirements: System requirements are dependent on operating system and need to be installed manually beforehand. Python requirements will be installed inside a virtual environment (strongly recommended) during setup.


#### System Requirements

* Python 3.6 incl. development tools
* Virtualenv
* poppler
* for production using uwsgi:
  * C compiler e.g. gcc
  * uwsgi
  * uwsgi Python3 plugin
* for production using Apache (in addition to uwsgi)
  * the mod proxy uwsgi plugin for apache2


#### Python Requirements

Python requirements are listed in ``requirements.txt``. They can be installed with pip using ``-r requirements.txt``.


### Development Setup

* create a new directory that should contain the files in future, e.g. ``mkdir collab-coursebook``
* change into that directory ``cd collab-coursebook``
* clone this repository ``git clone URL .``


**Automatic Setup**

1. execute the setup bash script ``Utils/setup.sh``
1. if you are using Windows install magic-bin ``pip install python-magic-bin`` (skip, if you are using Linux)


**Manual Setup**

1. setup a virtual environment using the proper python version ``virtualenv venv -p python3``
1. activate virtualenv ``source venv/bin/activate``
1. install python requirements ``pip install -r requirements.txt``
1. if you are using Windows, install python magic-bin ``pip install python-magic-bin`` (skip, if you are using Linux)
1. setup necessary database tables etc. ``python manage.py migrate``
1. prepare static files (can be omitted for dev setups) ``python manage.py collectstatic``
1. compile translations ``python manage.py compilemessages``
1. create a priviledged user, credentials are entered interactively on CLI ``python manage.py createsuperuser``
1. deactivate virtualenv ``deactivate``


**Development Server**

To start the application for development use ``python manage.py runserver 0:8000`` from the root directory.
*Do not use this for deployment!*

In your browser, access ``http://127.0.0.1:8000/`` and continue from there.


### Deployment Setup

This application can be deployed using a web server as any other Django application.
Remember to use a secret key that is not stored in any repository or similar, and disable DEBUG mode (``settings.py``).

**Step-by-Step Instructions**

1. log into your system with a sudo user
1. install system requirements
1. create a folder, e.g. ``mkdir /srv/collab-coursebook/``
1. change to the new directory ``cd /srv/collab-coursebook/``
1. clone this repository ``git clone URL .``
1. setup a virtual environment using the proper python version ``virtualenv venv -p python3``
1. activate virtualenv ``source venv/bin/activate``
1. update tools ``pip install --upgrade setuptools pip wheel``
1. install python requirements ``pip install -r requirements.txt``
1. create the file ``collab_coursebook/settings_secrets.py`` (copy from ``settings_secrets.py.sample``) and fill it with the necessary secrets (e.g. generated by ``tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c50``) (it is a good idea to restrict read permissions from others)
1. if necessary enable uwsgi proxy plugin for Apache e.g.``a2enmod proxy_uwsgi``
1. edit the apache config to serve the application and the static files, e.g. on a dedicated system in ``/etc/apache2/sites-enabled/000-default.conf`` within the ``VirtualHost`` tag add:

    ```
    Alias /static /srv/collab-coursebook/static
    <Directory /srv/collab-coursebook/static>
    Require all granted
    </Directory>

    ProxyPassMatch ^/static/ !
    ProxyPass / uwsgi://127.0.0.1:3035/
    ```

or create a new config (.conf) file (similar to ``apache-collab-coursebook.conf``) replacing $SUBDOMAIN with the subdomain the system should be available under, and $MAILADDRESS with the e-mail address of your administrator and $PATHTO with the appropriate paths. Copy or symlink it to ``/etc/apache2/sites-available``. Then activate it with ``a2ensite collab-coursebook``.


1. restart Apache ``sudo apachectl restart``
1. create a dedicated user, e.g. ``adduser django --disabled-login``
1. transfer ownership of the folder to the new user ``chown -R django:django /srv/collab-coursebook``
1. Copy or symlink the uwsgi config in ``uwsgi-collab-coursebook.ini`` to ``/etc/uwsgi/apps-available/`` and then symlink it to ``/etc/uwsgi/apps-enabled/`` using e.g., ``ln -s /srv/collab-coursebook/uwsgi-collab-coursebook.ini /etc/uwsgi/apps-available/collab-coursebook.ini`` and ``ln -s /etc/uwsgi/apps-available/collab-coursebook.ini /etc/uwsgi/apps-enabled/collab-coursebook.ini``
1. test your uwsgi configuration file with``uwsgi --ini collab-coursebook.ini``
1. restart uwsgi ``sudo systemctl restart uwsgi``
1. execute the update script ``./Utils/update.sh --prod``


### Updates

To update the setup to the current version on the main branch of the repository use the update script ``utils/update.sh`` or ``utils/update.sh --prod`` in production.

Afterwards, you may check your setup by executing ``utils/check.sh`` or ``utils/check.sh --prod`` in production.


## Structure

This repository contains a Django project called collab_coursebook. The functionality is encapsulated into Django apps:

1. **base**: This app contains the general Django models used to represent courses, contents, etc.
1. **frontend**: This app provides everything the users see when reading or editing the content. It also contains a landing page.
1. **content**: This app provides models, rendering- and export code for the different supported types of contents.
1. **export**: This app contains export functions for the custom content collections (coursebooks).

## Developer Notes
* to regenerate translations use ````python manage.py makemessages -l de_DE --ignore venv````
* to create a data backup use ````python manage.py dumpdata --indent=2 > db.json --traceback````
