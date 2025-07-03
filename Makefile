PYTHON = python
MANAGE = $(PYTHON) manage.py

run:
	$(MANAGE) runserver

migrate:
	$(MANAGE) migrate

makemigrations:
	$(MANAGE) makemigrations

shell:
	$(MANAGE) shell

createsuperuser:
	$(MANAGE) createsuperuser

collectstatic:
	$(MANAGE) collectstatic --noinput

reset-db:
	rm -f db.sqlite3
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	$(MAKE) makemigrations
	$(MAKE) migrate

translate:
	$(MANAGE) makemessages -l ar
	$(MANAGE) compilemessages
