from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from accounts.models import User
from rest_framework import status
from django.db import IntegrityError
from categories.models import Categories

from categories.serializers import CategoriesSerializer
from items.serializers import ItemsWithCategorySerializer
from .serializers import UserSerializer, UserGetAllSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from accounts.permissions import IsSuperuser, IsSuperuserAllowGetForAll
from accounts.models import User

class LoginView(APIView):

    def post(self, request):

        username= request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        user_type = ""

        if user:
            token = Token.objects.get_or_create(user=user)[0]

            user_logged = User.objects.get(username=username)

            if user_logged.is_superuser:
                user_type = 'superuser'
            else:
                user_type="user"

            return Response({'token': token.key, "user_id" : user_logged.id, "user_type" : user_type, "username" : user_logged.username })

        return Response({"message": "Wrong e-mail or password"}, status=status.HTTP_401_UNAUTHORIZED)


class SignupView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperuser]

    def post(self, request):

        try:
            new_user =  User.objects.create_user(
                username = request.data["username"],
                email = request.data["email"],
                password = request.data["password"],
                is_superuser = request.data["is_superuser"],
            )
        except IntegrityError:
            return Response({"User already exists"},status=status.HTTP_409_CONFLICT)

        serialized = UserSerializer(new_user)
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperuser]


    def get(self,request):

        users = User.objects.all()
        serialized = UserSerializer(users, many=True)

        return Response(serialized.data,status=status.HTTP_200_OK)


class UserDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperuserAllowGetForAll]

    def get(self,request, user_id=""):

        user = get_object_or_404(User, id=user_id)
        serialized = UserGetAllSerializer(user)

        return Response(serialized.data,status=status.HTTP_200_OK)


    def delete(self,request, user_id=""):

        user = get_object_or_404(User, id=user_id)
        user.delete()

        return Response({'message' : f"user {user_id} deleted"},status=status.HTTP_200_OK)


    def patch(self,request, user_id=""):

        user = get_object_or_404(User, id=user_id)
        serialized = UserSerializer(user, request.data, partial=True)
        fields = ["username", "email", "password", "is_superuser", 'password']
        wrong_fields = []

        for item in request.data:
            wrong_fields = []

            if item == 'password':
                return Response({'message' : 'This end-point does not update PASSWORD'} , status=status.HTTP_400_BAD_REQUEST)

            if item not in fields:
                wrong_fields.append(item)

        if len(wrong_fields) > 0:

            return Response({'message' : {'wrong_fields' : wrong_fields}} , status=status.HTTP_400_BAD_REQUEST)

        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)

        return Response({'message' : 'Wrong parrameters'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperuser]

    def patch(self,request):

        user = get_object_or_404(User, id=int(request.data['id']))
        user.set_password(request.data['password'])
        user.save()

        return Response({"message" : "Password Reseted"}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self,request, user_id=""):

        user_logged = request.user.id

        if user_logged != user_id:
            return Response({"message" : "User can only change it`s own password"}, status=status.HTTP_401_UNAUTHORIZED)

        user = get_object_or_404(User, id=user_id)

        if not user.check_password(request.data['old_password']):
            return Response({"message" : "Old Password is wrong"}, status=status.HTTP_401_UNAUTHORIZED)

        user.set_password(request.data['new_password'])
        user.save()

        return Response({"message" : "Password Updated"}, status=status.HTTP_200_OK)


class MassiveLoadView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsSuperuser]

  def post(self, request, user_id = ""):

    destroyCategory = Categories.objects.filter(user = user_id)
    destroyCategory.delete()

    for category in request.data:

      eachCategory = {
        "category": category["category"],   
        "description": category["description"],
        "active": category["active"],
        "position" : category["position"],
        "user" : user_id

      }

      serialized = CategoriesSerializer( data = eachCategory)

      category_id = 0

      if serialized.is_valid():
           category_id = serialized.save()

      for item in category["items"]: 
        eachItem = {
          "title" : item["title"],
          "desc" : item["desc"],
          "active" : item["active"],
          "position" : item["position"],
          "price" : item["price"],
          "category" : category_id.id,
        }

        item_serialized = ItemsWithCategorySerializer(data= eachItem)

        if item_serialized.is_valid():
           item_serialized.save()

    user = User.objects.filter(id = user_id)

    user_serialized = UserGetAllSerializer(user, many=True)
    
    return Response({"message" : "done", "data" : user_serialized.data}, status=status.HTTP_201_CREATED)


