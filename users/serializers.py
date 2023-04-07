from rest_framework.serializers import ModelSerializer

from .models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('last_name', 'first_name', 'username', 'email')
        # fields = '__all__'


class UserModelSerializerFull(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
