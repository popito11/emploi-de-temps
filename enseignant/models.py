from django.db import models

# Create your models here.


class Professeur(models.Model):
    
    nom_prof=models.CharField( max_length=50)
    email=models.EmailField(null=True,max_length=50)
    telephone=models.IntegerField(null=True)
    nombre_seance=models.IntegerField(null=True)
    def __str__(self):
        return self.nom_prof


class Horaire(models.Model):    
    plage=models.CharField( max_length=50)
    def __str__(self):
        return self.plage


class Horaireprof(models.Model):

    Professeur=models.ForeignKey('Professeur', null=False,on_delete=models.CASCADE)
    Horaire=models.ForeignKey('Horaire', on_delete=models.CASCADE ,null=False)
    jour=models.CharField(max_length=10)
    

