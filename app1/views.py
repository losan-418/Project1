from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from app1.serializers import UserSerializer, GroupSerializer, UserCreateSerializer, LoginSerializer
from rest_framework.views import APIView
from django.contrib.auth import login as django_login, logout as django_logout
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

@api_view(['POST'])
def add_user(request):
    serializer=UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Status":"Added"},status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    queryset=User.objects.all()
    serializer=UserSerializer(queryset)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def update_user(request, id=None):
    queryset = User.objects.get(id=id)
    serializer=UserSerializer(queryset,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"Status": "Updated"}, status=status.HTTP_205_RESET_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser])
def delete_user(request,id=None):
    queryset=User.objects.get(id=id)
    del_u=queryset.delete()
    if del_u:
        return Response({"Status": "Deleted"}, status=status.HTTP_200_OK)
    return Response({"Status":"Deletion Failed"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        django_login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=200)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        django_logout(request)
        return Response(status=204)