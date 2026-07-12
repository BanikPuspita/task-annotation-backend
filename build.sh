#!/usr/bin/env bash

echo "🚀 Starting build process..."

# Install dependencies
pip install -r requirements.txt

# Run migrations
echo "📦 Running migrations..."
python manage.py makemigrations api
python manage.py migrate

# Seed the database with sample data
echo "🌱 Seeding database..."
python manage.py seed_data

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Create media directory
mkdir -p media/images

echo "✅ Build completed successfully!"

python manage.py shell -c "
from django.contrib.auth.models import User;
u='admin';
e='admin@example.com';
p='admin123';
if not User.objects.filter(username=u).exists():
    User.objects.create_superuser(u,e,p)
"