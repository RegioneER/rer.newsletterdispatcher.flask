==============================
rer.newsletterdispatcher.flask
==============================

.. image:: https://travis-ci.com/RegioneER/rer.newsletterdispatcher.flask.svg?branch=master
    :target: https://travis-ci.com/RegioneER/rer.newsletterdispatcher.flask


A separate mail dispatcher for `rer.newsletter`__.

__https://github.com/RegioneER/rer.newsletter

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

Usage
-----

Flask app is a simple rest api with only one endpoint (*/add-to-queue*) that takes a list of parameters and add a job to the 
queue with these parameters.

Once the job is ready to be executed, it will send a list of emails with infos passed in parameters.

Needed parameters for this route are:

- _authenticator
- channel_url
- mfrom
- send_uid
- subject
- subscribers
- text

There is already a plugin for rer.newsletter called `rer.newsletterplugin.flask`__ that do this job.

__https://github.com/RegioneER/rer.newsletterplugin.flask

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

.. image:: https://www.redturtle.it/redturtle.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
