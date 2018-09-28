app=muckr_service

run:
	pipenv run env FLASK_APP=$(app) FLASK_ENV=development flask run

local:
	pipenv run heroku local

install:
	pip install pipenv
	pipenv install --dev --three
	pipenv install -e .

test:
	pipenv run py.test

clean:
	git clean -fxd
