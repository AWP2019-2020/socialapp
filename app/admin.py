from django.contrib import admin
from . import models
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
        list_display =('user', 'birthday')
        search_fields=('user__username',)

admin.site.register(models.Post)
admin.site.register(models.UserProfile, UserProfileAdmin) 