from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from categories.models import Categories
from categories.serializers import CategoriesSerializer, CategoriesWithItemsSerializer



class CategoriesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        categories = Categories.objects.all()
        serialized =  CategoriesWithItemsSerializer(categories, many=True)
#
        return Response(serialized.data,status=status.HTTP_200_OK)



    def post(self, request):
  
        serialized = CategoriesSerializer(data=request.data)

  

        if request.user.id  != request.data["user"] and request.user.is_superuser == False:
          return  Response({"message" : "Only superusers can post for others"}, status=status.HTTP_401_UNAUTHORIZED)

        
        if serialized.is_valid():
            serialized.save()
            return  Response(serialized.data, status=status.HTTP_201_CREATED)

        else:   

            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoriesDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, category_id=""):

      category = get_object_or_404(Categories,id=category_id)

      if request.user.id  != category.user.id and request.user.is_superuser == False:
          return  Response({"message" : "Only superusers can delete for others"}, status=status.HTTP_401_UNAUTHORIZED)

      category.delete()

      return Response({"message" : f"category {category_id} deleted"},status=status.HTTP_200_OK)


    def patch(self, request, category_id=""):

      if not request.data:
        return Response({"message": "You sent no options to update"},status=status.HTTP_400_BAD_REQUEST)

      category = get_object_or_404(Categories, id= category_id)
      serialized = CategoriesWithItemsSerializer(category, request.data, partial=True)
      if serialized.is_valid():
        serialized.save()

      return Response(serialized.data,status=status.HTTP_200_OK)

