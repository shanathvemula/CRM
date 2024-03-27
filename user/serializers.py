from rest_framework.serializers import ModelSerializer
from user.models import User, UserAddress # , Tasks


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserAddressSerializer(ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'
