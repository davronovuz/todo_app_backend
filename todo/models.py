from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
