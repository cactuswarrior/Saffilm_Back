from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer, UserInfoSerializer
from django.contrib.auth import get_user_model


@api_view(['POST'])
def signup(request):
	
    password = request.data.get('password')
    password_confirmation = request.data.get('passwordConfirmation')
	
    if password != password_confirmation:
        return Response({'error': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
		
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()

        user.set_password(request.data.get('password'))
        user.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def userinfo(request):
    
    users = get_user_model().objects.all()
    serializer = UserInfoSerializer(users, many=True)
    # print(serializer)
    return Response(serializer.data, status=200)
