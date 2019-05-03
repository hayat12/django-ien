from django.contrib import admin
from myapp.models import UserProfile, Event, Connection

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Connection)
