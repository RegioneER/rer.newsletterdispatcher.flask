.PHONY: dev
dev:
	FLASK_APP=app.py  bin/flask run

prod:
	bin/gunicorn -c gunicorn_config.py production:app
