.PHONY: dev
dev:
	FLASK_ENV=development FLASK_APP=app.py  bin/flask run

prod:
	bin/gunicorn -c gunicorn_config.py production:app

test:
	TESTING=true bin/pytest
