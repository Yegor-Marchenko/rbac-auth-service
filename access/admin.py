from django.contrib import admin
from .models import AccessRule, Resource, Role

admin.site.register(AccessRule)
admin.site.register(Resource)
admin.site.register(Role)