from rest_framework import serializers, fields

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        return User.objects.create_user(**validated_data)


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


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('id', 'members', 'created_at', 'description')


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('id', 'text', 'chat', 'author', 'created_at', 'is_read', 'membership')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('id', 'user', 'role', 'img', 'first_name', 'last_name', 'date_of_birth', 'gender', 'description',
                  'status')
