from django.db import models

# Create your models here.

class salle(models.Model):
    name=models.CharField(max_length=50)
    nombre_place=models.IntegerField(null=False)
    
    def __str__(self):
        return self.name
    
