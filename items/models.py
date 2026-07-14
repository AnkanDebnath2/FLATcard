from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()

    Location= models.TextField(blank=True, null=True)

    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='items_images', blank=True, null=True)
   

    "image = models.ImageField(upload_to='items_images', blank=True, null=True)"


    def __str__(self):
        return self.name
    


class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='items/')

    def __str__(self):
        return f"Image for {self.item.name}"     
   



    