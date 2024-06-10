from django.db import models

# Create your models here.
# https://www.techwithtim.net/tutorials/django/sqlite3-database/
# https://www.geeksforgeeks.org/django-model-data-types-and-fields-list/
# https://pythonistaplanet.com/django-database-tutorial/
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Models
# https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms
# https://www.techwithtim.net/tutorials/django/sqlite3-database/


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length = 10)

    def __str__(self):
        return self.ticker
