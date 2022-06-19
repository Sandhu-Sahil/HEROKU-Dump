from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Employee(models.Model):
    user = models.ForeignKey("User", on_delete=models.PROTECT)
    company = models.ForeignKey("Company", on_delete=models.PROTECT, null=True)
    join_date = models.DateTimeField(auto_now_add = True)

class Company(models.Model):
    name = models.CharField(max_length=1000)
    creator = models.ForeignKey("User", on_delete=models.PROTECT)

class History(models.Model):
    user = models.ForeignKey("User", on_delete=models.PROTECT )
    company = models.ForeignKey("Company", on_delete=models.PROTECT)
    join_date = models.DateTimeField(blank = True)
    leave_date = models.DateTimeField(auto_now_add = True)


