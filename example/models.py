from django.db import models

# Create your models here.
# https://www.techwithtim.net/tutorials/django/sqlite3-database/
# https://www.geeksforgeeks.org/django-model-data-types-and-fields-list/
# https://pythonistaplanet.com/django-database-tutorial/
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
# https://www.techwithtim.net/tutorials/django/sqlite3-database/


class Ships(models.Model):
    id = models.AutoField(primary_key=True)
    ship_name = models.CharField(max_length=100)
    ship_class= models.CharField(max_length=100)
    ship_race= models.CharField(max_length=100)
    ship_price= models.CharField(max_length=100)
    ship_weapon= models.CharField(max_length=100)
    ship_turret= models.CharField(max_length=100)
    ship_hull= models.CharField(max_length=100)
    ship_cargo= models.CharField(max_length=100)
    ship_dock= models.CharField(max_length=100)
    ship_hangar= models.CharField(max_length=100)
    ship_dlc= models.CharField(max_length=100)
    ship_role= models.CharField(max_length=100)
    ship_shield= models.CharField(max_length=100)
    ship_speed= models.CharField(max_length=100)
  

    def __str__(self):
        return self.ticker
