from rest_framework import serializers
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    class Model:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role'
        )


class NoAdminSerializers(serializers.ModelSerializer):
    class Model:
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role'
        )


class GetTokenSerializers(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True
    )
    confirmation_code = serializers.CharField(
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'confirmation_code'
        )


class SignUpSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username',)
