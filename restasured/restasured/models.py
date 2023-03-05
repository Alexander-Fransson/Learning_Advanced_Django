from django.db import models

class Drink(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)

    #To return their names as headers on admin page
    def __str__(self):
        return self.name
