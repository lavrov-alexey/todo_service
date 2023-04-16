from rest_framework.serializers import ModelSerializer

from .models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        # fields = ('last_name', 'first_name', 'username', 'email')
        fields = '__all__'


class UserModelSerializerVer2(ModelSerializer):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'username', 'email', 'is_staff', 'is_superuser')
