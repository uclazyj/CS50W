from django.contrib import admin
from .models import User, PlayerIcon, Image

# Register your models here.
admin.site.register(User)
admin.site.register(PlayerIcon)
admin.site.register(Image)