from django.db import models
from .category import Category

class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    img = models.ImageField(upload_to='images/products/', null=True, blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_all_product():
        return Product.objects.all()

    @property
    def imgURL(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url

    @staticmethod
    def get_categories_by_id(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_items()