from django.db import models

from config.constants import MAX_LENGTH


class Role(models.Model):
    title = models.CharField(max_length=MAX_LENGTH, unique=True)

    def __str__(self):
        return self.title

class Resource(models.Model):
    title = models.CharField(max_length=MAX_LENGTH, unique=True)

    def __str__(self):
        return self.title


class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    create_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)
    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['role', 'resource'],
                                    name='unique_role_resource')
        ]

    def __str__(self):
        return f'правило для {self.role} по объекту {self.resource}'
