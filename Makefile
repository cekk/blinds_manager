.PHONY: install
install:
	pipenv install

.PHONY: dev
dev:
	pipenv run python app.py