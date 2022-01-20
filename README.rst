kkanbu
======

kkanbu project

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/cookiecutter/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

:License: MIT

API Docs (OpenAPI 3.0)
----------------------

::

    http://127.0.0.1:8000/api/schema/swagger-ui/

First Setting the Environment with docker (Recommended)
--------------------------------------------------------

* install docker & docker-compose

* run docker

* build & run::

    $ docker-compose -f local.yml build
    $ docker-compose -f local.yml up


Initializing DataBase
--------------

* docker-compose로 실행시킨 모든 컨테이너 종료
* 모든 컨테이너 일괄 삭제::

    $ docker container prune
* postgres volume 삭제::

    $ docker volume rm teameet_backend_local_postgres_data
    $ docker volume rm teameet_backend_local_postgres_data_backups

* 컨테이너 재생성::

    $ docker-compose -f local.yml build



Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

HOW TO Command in DOCKER
^^^^^^^^^^^^^^^^^^^^^
As with any shell command that we wish to run in our container, this is done using this command::

    $ docker-compose -f local.yml run --rm django


Setting Up Your Database
^^^^^^^^^^^^^^^^^^^^^
Execute management commands::

    $ docker-compose -f local.yml run --rm django python manage.py migrate



Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ docker-compose -f local.yml run --rm django python manage.py createsuperuser


For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.   
    

----------------------------------------------------------------(update needed below)

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy kkanbu

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html

Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd kkanbu
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.

Deployment
----------

The following details how to deploy this application.

Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
