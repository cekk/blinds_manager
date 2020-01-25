.PHONY: install
install:
	pipenv install
	pipenv run buildout -N

.PHONY: buildout
buildout:
	pipenv run buildout -N

.PHONY: dev
dev:
	FLASK_APP=dev.py bin/flask run -p 8000

prod:
	bin/gunicorn -c gunicorn_config.py wsgi:app

deploy_lambda:
	pipenv run pip install --target ./lambda_function/package -r lambda_function/requirements.txt
	cd lambda_function/package && zip -r9 ../../function.zip .
	cd lambda_function && zip -g ../function.zip lambda_function.py
	cd lambda_function && zip -g ../function.zip capabilities_settings.py
	cd lambda_function && zip -r9 -g ../function.zip alexa
	aws2 lambda update-function-code --function-name gestore_tapparelle --zip-file fileb://function.zip
