from rest_framework import routers

from .views import *


router = routers.DefaultRouter()

router.register('consultations', ConsultationViewSet, basename='consultations')
router.register('services', ServiceViewSet, basename='services')
