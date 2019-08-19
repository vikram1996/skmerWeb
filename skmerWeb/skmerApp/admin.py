from django.contrib import admin
from .models import *


#table views

class skmerUserAdmin(admin.ModelAdmin):
    list_display= ('username', 'password','email')



# Register your models here.
admin.site.register(skmerUser,skmerUserAdmin)
