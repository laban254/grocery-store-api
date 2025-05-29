from django.db import migrations


def update_content_type(apps, schema_editor):
    ContentType = apps.get_model('contenttypes', 'ContentType')
    # Update content types
    ContentType.objects.filter(app_label='customers').update(app_label='accounts')
    
    # Update the django_migrations table directly
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("UPDATE django_migrations SET app = 'accounts' WHERE app = 'customers'")


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_content_type),
    ]
