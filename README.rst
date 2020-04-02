==============================
rer.newsletterdispatcher.flask
==============================

.. image:: https://travis-ci.com/RegioneER/rer.newsletterdispatcher.flask.svg?branch=master
    :target: https://travis-ci.com/RegioneER/rer.newsletterdispatcher.flask


Development
-----------

- Creare un proprio ambiente di sviluppo (venv, virtualenv, whatever...).
- Lanciare il buildout: ``bin/buildout``


- Per avviare ``redis``: ``./bin/redis-server``
- Per avviare ``rq`` (**dopo** redis): ``./bin/rq worker``
- Per avviare l'app ``flask``: ``make dev``
