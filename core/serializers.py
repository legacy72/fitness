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


class ProbeUserSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    probe_type_name = serializers.StringRelatedField(
        many=False,
        source='probe_type',
        read_only=True,
    )

    class Meta:
        model = Probe
        fields = ('id', 'user', 'probe_type', 'probe_type_name', 'value', 'created_at')


class ProbeSerializer(serializers.ModelSerializer):
    probe_type_name = serializers.StringRelatedField(
        many=False,
        source='probe_type',
        read_only=True,
    )

    class Meta:
        model = Probe
        fields = ('id', 'user', 'probe_type', 'probe_type_name', 'value', 'created_at')


class ProbeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProbeType
        fields = '__all__'
