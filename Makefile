.PHONY: install
install:
	pipenv install

.PHONY: dev
dev:
	pipenv run python app.py

prod:
	pipenv run gunicorn -c gunicorn_config.py wsgi:app