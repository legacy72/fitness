from rest_framework import routers

from .views import *


router = routers.DefaultRouter()


router.register('users', UserViewSet, basename='users')
router.register('roles', RoleViewSet, basename='roles')
router.register('user_probes', ProbeUserViewSet, basename='user_probes')
router.register('probes', ProbeViewSet, basename='probes')
router.register('probe_types', ProbeTypeViewSet, basename='probe_types')
