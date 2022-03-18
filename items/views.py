from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from items.models import Items
from items.serializers import ItemsSerializer


class ItemsView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):

        items = Items.objects.all()
        serialized =  ItemsSerializer(items, many=True)
        return Response(serialized.data,status=status.HTTP_200_OK)


    def post(self, request):
        serialized = ItemsSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return  Response(serialized.data, status=status.HTTP_201_CREATED)

        else:   
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemsDetailView(APIView):


  def delete(self, request, item_id=""):

    return Response({"Message":"Deletou item"},status=status.HTTP_200_OK)


  def patch(self, request, item_id=""):

    return Response({"Message":"atualizou item"},status=status.HTTP_200_OK)

