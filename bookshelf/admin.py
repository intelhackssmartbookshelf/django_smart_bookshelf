from django.contrib import admin
from .models import MyShelf, MyBooks, FcmToken

# Register your models here.
admin.site.register(MyShelf)
admin.site.register(MyBooks)
admin.site.register(FcmToken)