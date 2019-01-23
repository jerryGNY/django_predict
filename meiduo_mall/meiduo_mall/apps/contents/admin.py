from django.contrib import admin

# Register your models here.
from contents.models import ContentCategory, Content

admin.site.register(ContentCategory)
admin.site.register(Content)
