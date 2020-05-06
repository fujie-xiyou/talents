from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True, db_column="id")
    username = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=35)
