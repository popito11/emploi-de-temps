from django.shortcuts import render
from django.http import HttpResponse
from .models import MatiereProfesseur




def affiche_matiere_prof(request):
    mat_prof=MatiereProfesseur.objects.all()
    context={'matiere_prof':mat_prof}
    return render(request,'enseignant_matiere/enseignant_matiere.html',context)

# Create your views here.
