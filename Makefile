run:
	python manage.py runserver

db:
	python manage.py makemigrations
	python manage.py migrate

seed:
	python manage.py seeder


user:
	python manage.py createsuperuser