from django.db import migrations


def seed_access_rules(apps, schema_editor):
    Role = apps.get_model('authentication', 'Role')
    Resource = apps.get_model('authentication', 'Resource')
    AccessRule = apps.get_model('authentication', 'AccessRule')

    db_alias = schema_editor.connection.alias

    user_role = Role.objects.using(db_alias).get(title='user')
    admin_role = Role.objects.using(db_alias).get(title='admin')

    for title in ('order', 'review'):
        resource, _ = Resource.objects.using(db_alias).get_or_create(
            title=title
        )

        AccessRule.objects.using(db_alias).get_or_create(
            role=user_role,
            resource=resource,
            defaults={
                'read_permission': True,
            },
        )

        AccessRule.objects.using(db_alias).get_or_create(
            role=admin_role,
            resource=resource,
            defaults={
                'create_permission': True,
                'read_permission': True,
                'read_all_permission': True,
                'update_permission': True,
                'update_all_permission': True,
                'delete_permission': True,
                'delete_all_permission': True,
            },
        )


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_seed_roles'),
    ]

    operations = [
        migrations.RunPython(
            seed_access_rules,
            migrations.RunPython.noop,
        ),
    ]
