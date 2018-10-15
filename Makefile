app=muckr-service

flask-run:
	pipenv run env FLASK_ENV=development flask run

flask-shell:
	pipenv run flask shell

heroku-local:
	pipenv run heroku local

heroku-secretkey:
	pipenv run heroku config:set --app=$(app) SECRET_KEY=$$(pipenv run python -c 'import secrets; print(secrets.token_urlsafe())')

heroku-logs:
	pipenv run heroku logs --app=$(app)

travis-install:
	pip install pipenv
	pipenv install --dev --three
	pipenv install -e .

travis-script: test

test:
	pipenv run python -m flake8
	pipenv run py.test tests --verbose --cov=muckr

env-secretkey:
	echo SECRET_KEY=$$(pipenv run python -c 'import secrets; print(secrets.token_urlsafe())') >> .env

clean:
	git clean -fxd
