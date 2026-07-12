#!/usr/bin/env bash

pip install -r requirements.txt

python manage.py migrate

python manage.py collectstatic --noinput

mkdir -p media/images

python manage.py shell -c "
from django.contrib.auth.models import User;
u='admin';
e='admin@example.com';
p='admin123';
if not User.objects.filter(username=u).exists():
    User.objects.create_superuser(u,e,p)
"