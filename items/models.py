from django.db import models
class Items (models.Model):

    title = models.CharField(max_length=255, null=False)
    desc = models.CharField(max_length=255,null=True, blank=True, default='')
    active = models.BooleanField(null=False)
    price = models.CharField(max_length=6, null=True,  blank=True, default='')
    position = models.IntegerField(null=False)
    category = models.ForeignKey('categories.Categories', on_delete=models.CASCADE, related_name="items")