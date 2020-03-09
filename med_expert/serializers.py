from rest_framework import serializers, fields

from .models import *

class ConsultationSerializer(serializers.ModelSerializer):
    date_create = fields.DateTimeField(input_formats=['%d.%m.%Y'])
    date_provision = fields.DateTimeField(input_formats=['%d.%m.%Y'])
    date_finish = fields.DateTimeField(input_formats=['%d.%m.%Y'])

    class Meta:
        model = Consultation
        fields = (
            'name',
            'date_create',
            'date_provision', 
            'date_finish',
            'cost', 
            'status', 
            'client',
            'expert',
        )
