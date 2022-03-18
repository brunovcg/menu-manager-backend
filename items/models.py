from django.db import models
class Items (models.Model):

    title = models.CharField(max_length=255, null=False)
    itemId = models.CharField(max_length=255, unique=True, null=False)
    desc = models.CharField(max_length=255)
    active = models.BooleanField(null=False)
    position = models.BooleanField(null=False)
    category = models.ForeignKey('categories.Categories', on_delete=models.CASCADE, related_name="items")