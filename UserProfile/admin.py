from django.contrib import admin

from .models import Profile, status, friend, notification, coverphotos, profilephotos, Response, Liker, comments, \
    replies


class statusAdmin(admin.ModelAdmin):
    list_display=['post','date','day','time']
admin.site.register(Profile)
admin.site.register(status,statusAdmin)
admin.site.register(friend)
admin.site.register(notification)
admin.site.register(Response)
admin.site.register(Liker)
admin.site.register(comments)
admin.site.register(replies)
admin.site.register(coverphotos)
admin.site.register(profilephotos)

