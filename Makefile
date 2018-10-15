flask-run:
	pipenv run env FLASK_ENV=development flask run

heroku-local:
	pipenv run heroku local

travis-install:
	pip install pipenv
	pipenv install --dev --three
	pipenv install -e .

travis-script:
	pipenv run python tests/test_app.py

generate-secretkey:
	@pipenv run python -c 'import secrets; print("SECRET_KEY={}".format(secrets.token_urlsafe()))'

clean:
	git clean -fxd
