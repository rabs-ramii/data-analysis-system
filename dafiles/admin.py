from django.contrib import admin
from dafiles.models import File
# Register your models here.

class FileAdmin(admin.ModelAdmin):
    list_display=("id","file")

admin.site.register(File,FileAdmin)
