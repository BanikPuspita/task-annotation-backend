#!/usr/bin/env bash
set -e

echo "🚀 Starting build process..."

# Run migrations
echo "📦 Running migrations..."
python manage.py makemigrations api
python manage.py migrate

# Ensure demo admin user exists (never wipe existing data)
echo "👤 Ensuring admin user exists..."
python manage.py shell -c "
from django.contrib.auth.models import User;
u='admin';
e='admin@example.com';
p='admin123';
user, created = User.objects.get_or_create(username=u, defaults={'email': e});
if created:
    user.set_password(p);
    user.is_staff = True;
    user.is_superuser = True;
    user.save();
    print('Created admin user');
else:
    print('Admin user already exists');
"

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create media directory
mkdir -p media/images

echo "✅ Build completed successfully!"
