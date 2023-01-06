from django.contrib import admin
from solo.admin import SingletonModelAdmin
from youtube.models import Channel, Video, FeedSettings

admin.site.register(FeedSettings, SingletonModelAdmin)

admin.site.register(Channel)
admin.site.register(Video)
