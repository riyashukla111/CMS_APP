from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Post,Like
from .serializers import CreatePostSerializer, GetPostSerializer,LikePostSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    request.data["created_by"] = request.user.id
    post_serializer = CreatePostSerializer(data=request.data)
    if post_serializer.is_valid():
        post_serializer.save()
        return Response(post_serializer.data, status=status.HTTP_201_CREATED)
    return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_posts(request, id=None):
    post = Post.objects.filter(Q(created_by=request.user.id) | Q(is_public=True))
    print(request.user.id)
    if id is not None:
        post = post.filter(id=id)
    post_serializer = GetPostSerializer(post,many=True)
    return Response(post_serializer.data,status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.created_by.id == request.user.id:
        serializer = CreatePostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'msg':'Not Created by the current User'},status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if post.created_by.id == request.user.id:
        post.delete()
        return Response({'msg':'Deleted Successfully'},status=status.HTTP_200_OK)
    return Response({'msg':'Not Created by the current User'},status=status.HTTP_401_UNAUTHORIZED)


# API FOR LIKE MODEL
    
@api_view(['GET'])
def get_likes(request, post_id):
    user_like = False
    post = Like.objects.filter(post_id=post_id)
    if request.user and post.filter(user_id=request.user.id):
        user_like = True
    likes_count = post.count()
    return Response({'likes count':likes_count,'user like':user_like}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def give_like(request, post_id):
    post = Post.objects.get(id=post_id)
    if post and not Like.objects.filter(user_id=request.user, post_id=post):
        like_obj = Like(post_id=post, user_id=request.user) 
        like_obj.save()
        return Response({'msg':f"{request.user.username} like the {post.title}"}, status=status.HTTP_201_CREATED)
    return Response({'error':'Cannot like the post'},status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_like(request, post_id):
    like = get_object_or_404(Like, post_id=post_id, user_id=request.user.id)
    if like:
        like.delete()
        return Response({'msg':'Like Deleted Successfully'},status=status.HTTP_200_OK)
    return Response({'msg':'Invalid Details'},status=status.HTTP_401_UNAUTHORIZED)
    
