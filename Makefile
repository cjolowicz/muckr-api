PYTHON=python3.7
app=muckr-service

all:

virtualenv:
	$(PYTHON) -m venv venv

requirements/%.txt: requirements/%.in
	pip install pip-tools
	python -m piptools compile \
	    --verbose \
	    --upgrade \
	    --output-file=$@ $<

requirements: requirements/base.txt requirements/dev.txt

install:
	pip install \
	    --requirement requirements/base.txt \
	    --requirement requirements/dev.txt

black:
	black muckr tests setup.py wsgi.py migrations

test:
	python -m flake8 muckr tests setup.py wsgi.py migrations
	env FLASK_DEBUG=0 python -m pytest tests --cov=muckr --cov-report=term-missing

clean:
	for dir in muckr tests ; \
	do \
	    find "$$dir" \
	        -name '*.pyc' -print0 -or \
	        -name '__pycache__' -print0 -or \
	        -false | xargs -0 rm -vrf ; \
	done

distclean:
	git clean -fxd

heroku-secretkey:
	heroku config:set --app=$(app) SECRET_KEY=$$(python -c 'import secrets; print(secrets.token_urlsafe())')

heroku-adminpassword:
	heroku config:set --app=$(app) ADMIN_PASSWORD=$$(python -c 'import secrets; print(secrets.token_urlsafe())')

heroku-db-upgrade:
	heroku run --app=$(app) flask db upgrade

travis-install: install

travis-script: test
	coveralls

env-secretkey:
	echo SECRET_KEY=$$(python -c 'import secrets; print(secrets.token_urlsafe())') >> .env

env-adminpassword:
	echo ADMIN_PASSWORD=$$(python -c 'import secrets; print(secrets.token_urlsafe())') >> .env
