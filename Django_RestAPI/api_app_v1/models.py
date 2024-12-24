from django.db import models


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=20)
    email = models.EmailField()
    age = models.IntegerField()

    def __str__(self):
        return f"{self.login} - {self.email}"


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=150)
    product_cnt = models.IntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    product_count = models.PositiveIntegerField()

    def __str__(self):
        return f"Cart for {self.user_id} with {self.product_name}"
