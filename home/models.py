from django.db import models


# Create your models here.


class Menu(models.Model):
    id =  models.AutoField(primary_key=True)
    menu_name =  models.CharField(max_length=50, null=False)
    title =  models.CharField(max_length=300, null=False)
    icon =  models.CharField(max_length=200, null=False)

    def __str__(self):
        return self.menu_name

    class Meta:
        db_table ='menus'



class Month(models.Model):
    id =  models.AutoField(primary_key=True)
    month_name  = models.CharField(max_length=50)
    month_id = models.IntegerField()

    def __str__(self):
        return self.month_name
    class Meta:
        db_table ='months'