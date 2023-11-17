from django.db import models

# Create your models here.

class Matiere(models.Model):
    nom_matiere=models.CharField(max_length=20)
    code=models.CharField(max_length=20)
    niveau=models.IntegerField()
    nb_eleve=models.IntegerField()
    nb_seance=models.IntegerField()
    optionnel = models.BooleanField(default=False)
    
    def __str__(self):
        return self.nom_matiere


