from django.contrib import admin
from subject.models import Subject, SubOption, SubType

admin.site.register(Subject)
admin.site.register(SubOption)
admin.site.register(SubType)
# admin.site.register(Answer)