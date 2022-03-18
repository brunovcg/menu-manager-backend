from rest_framework import serializers
from accounts.models import User
from categories.serializers import CategoriesWithItemsSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'is_superuser']


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserGetAllSerializer(serializers.ModelSerializer):

  categories = CategoriesWithItemsSerializer(many=True)
  class Meta:
   model = User
   fields = ['id','username', 'email', 'is_superuser', "categories"]
   
