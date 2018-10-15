app=muckr_service

flask-run:
	pipenv run env FLASK_APP=$(app) FLASK_ENV=development flask run

heroku-local:
	pipenv run heroku local

travis-install:
	pip install pipenv
	pipenv install --dev --three
	pipenv install -e .

travis-script:
	pipenv run python tests/test_app.py

clean:
	git clean -fxd
