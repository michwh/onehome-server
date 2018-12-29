from django.db import models

# Create your models here.

class Product(models.Model):
    user_name = models.CharField(max_length=128)
    user_image_URL = models.ImageField(upload_to='static/userImages', null=True)
    c_time = models.DateTimeField(auto_now_add=True)
    goods_price = models.CharField(max_length=20)
    title = models.CharField(max_length=100, verbose_name="标题")
    description = models.TextField(verbose_name="商品描述", max_length=300)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "商品"
        verbose_name_plural = "商品"


class ProductImags(models.Model):
    c_time = models.DateTimeField(auto_now_add=True)
    pictures1 = models.ImageField(upload_to='static/productImages')
    pictures2 = models.ImageField(upload_to='static/ProductImages', null=True)
    pictures3 = models.ImageField(upload_to='static/ProductImages', null=True)
    pictures4 = models.ImageField(upload_to='static/ProductImages', null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "商品图片"
        verbose_name_plural = "商品图片"
