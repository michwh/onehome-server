from django.db import models
from users.models import User
from product.models import Product


class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "收藏"
        verbose_name_plural = "收藏"
