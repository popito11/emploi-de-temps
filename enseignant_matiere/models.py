
from django.db import models
from matiere.models import Matiere
from enseignant.models import Professeur


# Create your models here.

class MatiereProfesseur(models.Model):
    Professeur = models.ForeignKey(Professeur, null=False, on_delete=models.CASCADE)
    Matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, null=False)
