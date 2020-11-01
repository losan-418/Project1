from django.contrib.auth.models import User, Group
from rest_framework import serializers,exceptions
from django.contrib.auth import authenticate
from app1.models import UserModel


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [ 'id','username', 'email', 'groups',]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups','password']

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username= username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is not logged in."
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Please provide username and password."
            raise exceptions.ValidationError(msg)
        return data