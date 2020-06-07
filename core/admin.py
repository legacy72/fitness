from django.contrib import admin

from .models import *


admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Role)
admin.site.register(MemberShip)
admin.site.register(Message)
admin.site.register(Chat)
admin.site.register(ProbeType)
admin.site.register(Probe)
admin.site.register(AuthCode)
