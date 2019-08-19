from django.contrib import admin
from .models import *



#table Views
class fileAdmin(admin.ModelAdmin):
    list_display= ('biologicalName' , 'createDateTime', 'fileExtension', 'createUser','fastQ')

class analysisAdmin(admin.ModelAdmin):
    list_display = ('createDateTime' , 'createUser', 'createInputFile', 'analysis','distanceEdit' , 'distanceJukesCantor')

# Register your models here.
admin.site.register(inputQueryFile,fileAdmin)
admin.site.register(analysisFile,analysisAdmin)