from rest_framework import serializers
from .models import Categories
from items.serializers import ItemsSerializer


class CategoriesSerializer(serializers.ModelSerializer):

  class Meta:
    model = Categories
    fields = "__all__"


class CategoriesWithItemsSerializer(serializers.ModelSerializer):

    items = ItemsSerializer(many=True)

    class Meta:
      model = Categories
      exclude=["user"]