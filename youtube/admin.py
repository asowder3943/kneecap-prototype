from django.contrib import admin

from youtube.models import Channel, Video

admin.site.register(Channel)
admin.site.register(Video)