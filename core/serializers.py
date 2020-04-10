from rest_framework import serializers, fields

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # fields = (
        #     'username',
        #     'profile',
        # )


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class ProbeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Probe
        fields = '__all__'


class ProbeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbeType
        fields = '__all__'
