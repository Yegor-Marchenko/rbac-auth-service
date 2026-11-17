
from django.db import migrations


def seed_roles(apps, schema_editor):
    Role = apps.get_model('access', 'Role')
    db_alias = schema_editor.connection.alias

    for title in ('user', 'admin'):
        Role.objects.using(db_alias).get_or_create(title=title)


class Migration(migrations.Migration):

    dependencies = [
        ('access', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_roles, migrations.RunPython.noop),
    ]
