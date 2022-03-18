from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from categories.models import Categories
from categories.serializers import CategoriesSerializer


class CategoriesView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):

        categories = Categories.objects.all()
        serialized =  CategoriesSerializer(categories, many=True)

        return Response(serialized.data,status=status.HTTP_200_OK)


class CategoriesDetailView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def delete(self, request, category_id=""):

      return Response({"message" : "delete category"},status=status.HTTP_200_OK)


    def post(self, request, category_id=""):

      return Response({"message" : "post category"},status=status.HTTP_200_OK)

