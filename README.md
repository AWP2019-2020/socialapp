# socialapp
Django project example containing a social-app

Install virtualenv:

        virtualenv venv
        . venv/bin/activate

Install packages:

        pip install -r requirements.txt

Apply migrations:

        python manage.py migrate

Start project:

        django-admin startproject [project_name] [project_location]

**Example:** 

        django-admin.py startproject socialapp .

Start app

        python manage.py startapp [app_name]

Create migrations:

        python manage.py makemigrations

Start server:

        python manage.py runserver

### Stop server using CTRL+C

Create admin user (superuser):

        python manage.py createsuperuser
