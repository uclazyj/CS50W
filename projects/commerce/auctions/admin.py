from django.contrib import admin

from .models import User, Listing, Bid, Watch, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Watch)
admin.site.register(Comment)
