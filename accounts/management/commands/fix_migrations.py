from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Fixes migration issues when renaming customers app to accounts'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Update the django_migrations table
            cursor.execute("UPDATE django_migrations SET app = 'accounts' WHERE app = 'customers'")
            migrations_updated = cursor.rowcount
            self.stdout.write(self.style.SUCCESS(f'Updated {migrations_updated} rows in django_migrations'))
            
            # Update content types table
            cursor.execute("UPDATE django_content_type SET app_label = 'accounts' WHERE app_label = 'customers'")
            content_types_updated = cursor.rowcount
            self.stdout.write(self.style.SUCCESS(f'Updated {content_types_updated} rows in django_content_type'))
