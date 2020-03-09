from django.contrib import admin

from .models import *


admin.site.register(User)
admin.site.register(Expert)
admin.site.register(MedicalCenter)
admin.site.register(Consultation)
admin.site.register(Service)
