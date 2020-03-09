from django.shortcuts import render
from rest_framework import status, viewsets

from .models import *
from .serializers import *


class ConsultationViewSet(viewsets.ModelViewSet):
    """
    Вьюшка для получения всех консультаций юзера
    """
    serializer_class = ConsultationSerializer
    permission_classes = []

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = Consultation.objects.filter(client__id=user_id).all()
        else:
            queryset = Consultation.objects.all()
        return queryset


    def dispatch(self, request, *args, **kwargs):
        return super(ConsultationViewSet, self).dispatch(request, *args, **kwargs)
