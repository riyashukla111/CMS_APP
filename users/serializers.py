from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        # Extract the password from the validated data
        password = validated_data.pop('password', None)

        # Create the user object without saving it yet
        user = User(**validated_data)

        # Set the password using Django's built-in method,
        # which automatically hashes the password before saving.
        if password is not None:
            user.set_password(password)
            
        # Save the user object with the hashed password
        user.save()
        return user



# class SignupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
#         extra_kwargs = {'password': {'write_only': True}}