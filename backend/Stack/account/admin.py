from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Relation

UserAdmin.fieldsets[2][1]['fields'] = (
    'is_active',
    'is_staff',
    'is_superuser',
    'label_job',
    'image',
    'city',
    'bio',
    'groups',
    'user_permissions'
)
UserAdmin.list_display += ('label_job',
                           'image',
                           'city',
                           'bio',)

admin.site.register(User, UserAdmin)
admin.site.register(Relation)
