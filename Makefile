.PHONY: dev
dev:
	FLASK_APP=app.py bin/flask run -p 8000

prod:
	bin/gunicorn -c gunicorn_config.py production:app
