from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from categories.models import Categories
from items.models import Items
from items.serializers import ItemsSerializer, ItemsWithCategorySerializer
from django.shortcuts import get_object_or_404


class ItemsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):

        items = Items.objects.all()
        serialized =  ItemsWithCategorySerializer(items, many=True)
        return Response(serialized.data,status=status.HTTP_200_OK)


    def post(self, request):

        category = get_object_or_404(Categories, id= request.data["category"])

        if request.user.id  != category.user.id and request.user.is_superuser == False:
          return  Response({"message" : "Only superusers can post for others"}, status=status.HTTP_401_UNAUTHORIZED)
        serialized = ItemsWithCategorySerializer(data=request.data)
       
        if serialized.is_valid():
            serialized.save()
            return  Response(serialized.data, status=status.HTTP_201_CREATED)

        else:   
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemsDetailView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def delete(self, request, item_id=""):

    item = get_object_or_404(Items,id=item_id)


    if request.user.id  != item.category.user.id and request.user.is_superuser == False:
          return  Response({"message" : "Only superusers can delete for others"}, status=status.HTTP_401_UNAUTHORIZED)

    item.delete()
    return Response({"Message":f"Deletou item {item_id}"},status=status.HTTP_200_OK)


  def patch(self, request, item_id=""):

      if not request.data:
        return Response({"message": "You sent no options to update"},status=status.HTTP_400_BAD_REQUEST)

      items = get_object_or_404(Items, id= item_id)
      serialized =  ItemsWithCategorySerializer(items, request.data, partial=True)
      if serialized.is_valid():
        serialized.save()

      return Response(serialized.data,status=status.HTTP_200_OK)

