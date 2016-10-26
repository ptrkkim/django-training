from rest_framework import serializers

from src.core_auth.models import User


class RequestPasswordChangeSerializer(serializers.Serializer):
    email = serializers.EmailField(label='Email')

    def validate(self, attrs):
        try:
            attrs['user'] = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            pass
        return attrs


class ChangePasswordSerializer(serializers.Serializer):

    password_1 = serializers.CharField(label="New password", style={'input_type': 'password'})
    password_2 = serializers.CharField(label="Confirm new password", style={'input_type': 'password'})

    def validate(self, attrs):
        password_1, password_2 = attrs['password_1'], attrs['password_2']

        if not password_1 == password_2:
            raise serializers.ValidationError('Passwords must match.')

        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'needs_change_password']
