from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=255) 
    description = models.TextField() 
    image = models.ImageField(upload_to='products/') 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    visited = models.DateTimeField(default=timezone.now())
  
    def __str__(self): 
        return self.name 
    