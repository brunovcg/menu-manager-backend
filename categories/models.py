from django.db import models
class Categories (models.Model):

    category = models.CharField(max_length=255, null=False)
    categoryId = models.CharField(max_length=255, unique=True, null=False)
    description = models.CharField(max_length=255)
    active = models.BooleanField(null=False)
    position = models.BooleanField(null=False)
    user = models.ForeignKey('user.Users', on_delete=models.CASCADE, related_name="categories")