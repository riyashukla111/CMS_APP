from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Post
from users.serializers import UserSerializer

User = get_user_model()

class GetPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'content', 'is_public', 'created_date', 'created_by']

    # Optional: If you want to include the user's username in the serialized output
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    

class CreatePostSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'content', 'is_public', 'created_date', 'created_by']


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['post_id', 'user_id','created_date']
