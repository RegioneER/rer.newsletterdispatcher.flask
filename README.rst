.. image:: https://github.com/RegioneER/rer.newsletterdispatcher.flask/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/RegioneER/rer.newsletterdispatcher.flask/actions
    :alt: Tests

==============================
rer.newsletterdispatcher.flask
==============================

A separate mail dispatcher for `rer.newsletter <https://github.com/RegioneER/rer.newsletter>`_.


This is useful when you have channels with a lot of subscriptions (we had some with > 70000) and don't want to
block Plone instances to do this long job.

The dispatcher is a combination of three pieces:

- Flask app with flask-mail
- Redis (for job queues)
- Rq (a python library to manage redis queues and execute jobs)

These are three different processes that need to run together.

Installation
------------

All dependencies are managed with ``buildout``. There are two profiles for **development** and **production** environments.

The best way to install this application is with ``virtualenv`` or ``pyenv``.

Once we activated the virtualenv, we need to install basic requirements::


    > pip install -r requirements.txt

After that, you need to choose with profile you want to use (production.cfg or development.cfg)::

    > ln -s development.cfg buildout.cfg

And last but not least, you have to run the buildout::

    > bin/buildout -N

This will install all needed dependencies and after that, you will find all needed scripts into ``bin`` folder.

Run
---

In **development** mode you need to start all services individually:

- ``bin/redis-server`` to start redis server
- ``bin/rq worker`` to start rq (it needs a working redis instance)
- ``make dev`` to start Flask app in development mode

In **production** mode we use ``supervisor`` to manage all processes in background, so you only need to start redis daemon with::

    > bin/supervisord

And it will start and manage all services.


Custom configurations
---------------------

You can add a custom configuration for Flask app by adding the environments variables

For example if you want to customize Flask-Mail mail server address (default is localhost), you can create this environment variable::

   export RER_NEWSLETTERDISPATCHER_MAIL_SERVER="myserver.net"

You can set base Flask config parameters and some application-related ones:

- RER_NEWSLETTERDISPATCHER_MAIL_SERVER (mailserver address)
- RER_NEWSLETTERDISPATCHER_MAIL_PORT (mailserver port, 25 by default)[optional]
- RER_NEWSLETTERDISPATCHER_MAIL_USERNAME (mailserver client username)[optional]
- RER_NEWSLETTERDISPATCHER_MAIL_PASSWORD (mailserver cliend password)[optional]
- RER_NEWSLETTERDISPATCHER_SENTRY_DSN (sentry dsn value)
- RER_NEWSLETTERDISPATCHER_REDIS_PORT (port where redis should listen. Default is 6379 but it's better to change it)


Custom buildout configurations
------------------------------

You can run a buildout with some custom configurations like ports.

To do this, you only need to extend another buildout (for example *production.cfg*) and add your additional customizations::

    [buildout]
    extends =
        production.cfg

    [ports]
    gunicorn = 1111
    redis = 2222

After that you only need to re-run buildout with::

    bin/buildout -Nc name_of_cfg_file.cfg



Usage
-----

Flask app is a simple rest api with only one endpoint (*/add-to-queue*) that takes a list of parameters and add a job to the 
queue with these parameters.

Once the job is ready to be executed, it will send a list of emails with infos passed in parameters.

Needed parameters for this route are:

- channel_url
- mfrom
- send_uid
- subject
- subscribers
- text

You can also attach some files to the POST call and they will be send as mail attachments.

There is already a plugin for rer.newsletter called `rer.newsletterplugin.flask <https://github.com/RegioneER/rer.newsletterplugin.flask>`_ that do this job.


Security
--------

By default, this app accept only calls from localhost, so it does not need any other complex mechanisms.
It should run on the same sever where runs your Plone instances.

Credits
-------

Developed with the support of `Regione Emilia Romagna <http://www.regione.emilia-romagna.it/>`_;

Regione Emilia Romagna supports the `PloneGov initiative <http://www.plonegov.it/>`_.

Authors
-------

This product was developed by **RedTurtle Technology** team.

.. image:: https://avatars1.githubusercontent.com/u/1087171?s=100&v=4
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
