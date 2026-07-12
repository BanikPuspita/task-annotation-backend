from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Task
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seed the database with sample data (only if empty — never deletes existing data)'

    def handle(self, *args, **options):
        self.stdout.write('🌱 Seeding database...')

        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com'
            }
        )
        if created:
            user.set_password('admin123')
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(f'✅ Created user: {user.username}')

        if Task.objects.exists():
            self.stdout.write(self.style.WARNING(
                '⏭️  Tasks already exist — skipping seed to preserve your data.'
            ))
            return

        tasks = [
            {
                'title': 'Complete Project Documentation',
                'description': 'Write comprehensive documentation for the TaskFlow application including API docs and user guides.',
                'priority': 'HIGH',
                'status': 'TODO',
                'due_date': date.today() + timedelta(days=5),
                'task_date': date.today(),
                'tags': ['documentation', 'urgent']
            },
            {
                'title': 'Review Pull Requests',
                'description': 'Review and merge pending PRs from the team members.',
                'priority': 'MEDIUM',
                'status': 'IN_PROGRESS',
                'due_date': date.today() + timedelta(days=2),
                'task_date': date.today(),
                'tags': ['review', 'collaboration']
            },
            {
                'title': 'Fix Authentication Bug',
                'description': 'Fix the JWT token expiration issue reported by users.',
                'priority': 'HIGH',
                'status': 'IN_PROGRESS',
                'due_date': date.today() + timedelta(days=1),
                'task_date': date.today(),
                'tags': ['bug', 'authentication']
            },
            {
                'title': 'Deploy to Production',
                'description': 'Deploy the latest features to production environment.',
                'priority': 'HIGH',
                'status': 'DONE',
                'due_date': date.today() - timedelta(days=1),
                'task_date': date.today(),
                'tags': ['deployment', 'release']
            },
            {
                'title': 'Update UI Components',
                'description': 'Update the dashboard UI with new design system components.',
                'priority': 'LOW',
                'status': 'TODO',
                'due_date': date.today() + timedelta(days=7),
                'task_date': date.today(),
                'tags': ['ui', 'design']
            },
            {
                'title': 'Write Unit Tests',
                'description': 'Write comprehensive unit tests for the task management API.',
                'priority': 'MEDIUM',
                'status': 'TODO',
                'due_date': date.today() + timedelta(days=3),
                'task_date': date.today(),
                'tags': ['testing', 'quality']
            },
        ]

        created_count = 0
        for task_data in tasks:
            Task.objects.create(user=user, **task_data)
            created_count += 1
            self.stdout.write(f'  📝 Created task: {task_data["title"]}')

        self.stdout.write(self.style.SUCCESS(f'✅ Successfully created {created_count} tasks!'))
