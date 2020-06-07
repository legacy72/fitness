from rest_framework import routers

from .views import *


router = routers.DefaultRouter()


router.register('users', UserViewSet, basename='users')
router.register('roles', RoleViewSet, basename='roles')
router.register('user_probes', ProbeUserViewSet, basename='user_probes')
router.register('probes', ProbeViewSet, basename='probes')
router.register('probe_types', ProbeTypeViewSet, basename='probe_types')
router.register('chats', ChatViewSet, basename='chats')
router.register('messages', MessageViewSet, basename='messages')
router.register('profiles', ProfileViewSet, basename='profiles')
router.register('activate_user', ActivateUserView, basename='activate_user')
router.register('resend_code', ResendCodeView, basename='resend_code')
