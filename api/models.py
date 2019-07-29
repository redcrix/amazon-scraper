from django.db import models

class Input(models.Model):
    url=models.CharField(max_length=1000)
    page_no=models.IntegerField()

    def __str__(self):
        return self.url

class Api(models.Model):
    Product_name=models.CharField(max_length=50)
    by_info = models.CharField(max_length=15)
    Product_url = models.CharField(max_length=1000)
    Product_img = models.CharField(max_length=1000)
    Product_price = models.CharField(max_length=10)
    rating = models.CharField(max_length=15)
    total_review = models.CharField(max_length=15)
    ans_ask = models.CharField(max_length=15)
    prod_des = models.CharField(max_length=800)
    feature = models.CharField(max_length=1000)
    cust_review = models.CharField(max_length=5000)

    def __str__(self):
        return self.Product_name
