from django.contrib import admin
from .models import Register,Login,Blog,Notification

admin.site.register(Register)
admin.site.register(Login)

admin.site.register(Blog)
admin.site.register(Notification)

# Register your models here.
