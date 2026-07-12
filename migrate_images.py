import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from api.models import Image

def migrate_images():
    # Check if the columns exist
    with connection.cursor() as cursor:
        cursor.execute("PRAGMA table_info(api_image)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'image_url' not in columns:
            print("Adding image_url column...")
            cursor.execute("ALTER TABLE api_image ADD COLUMN image_url varchar(500) NULL")
        
        if 'public_id' not in columns:
            print("Adding public_id column...")
            cursor.execute("ALTER TABLE api_image ADD COLUMN public_id varchar(255) NULL")
        
        print("Migration complete!")

if __name__ == "__main__":
    migrate_images()