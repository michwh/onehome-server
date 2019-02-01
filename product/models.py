from django.db import models
from users.models import User

# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    c_time = models.DateTimeField(auto_now_add=True)
    goods_price = models.CharField(max_length=20)
    title = models.CharField(max_length=100, verbose_name="标题")
    description = models.TextField(verbose_name="商品描述", max_length=300)
    goods_img1 = models.CharField(max_length=100, null=False)
    goods_img2 = models.CharField(max_length=100, null=True)
    goods_img3 = models.CharField(max_length=100, null=True)
    goods_img4 = models.CharField(max_length=100, null=True)

    # 定义数据库的打印效果
    def __str__(self):
        return 'id:'+str(self.id)+',username:'+str(self.username)

    class Meta:
        # 返回的数据按时间排序
        ordering = ["-c_time"]
        verbose_name = "商品"
        verbose_name_plural = "商品"


# class Collection(models.Model):
#     id = models.AutoField(primary_key=True)
#     product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
#     username = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
#     c_time = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.id
#
#     class Meta:
#         ordering = ["-c_time"]
#         verbose_name = "收藏"

