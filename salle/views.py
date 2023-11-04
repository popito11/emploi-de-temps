from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import salle
from enseignant.models import Professeur
from matiere.models import Matiere





# Create your views here.

  

def ajouter_salle(request):
    
    if request.method=='POST':
        nom_salle=request.POST.get("nom")
        nombre_places=request.POST.get("nb_place")
        
        salles=salle(name=nom_salle,nombre_place=nombre_places)
        
        salles.save()
        return redirect('/')
    
    return render(request,'salle/salle_save.html')

def supprimer_salle(request,salle_id):
    
    salles=salle.objects.get(id=salle_id)
    if request.method=='POST':
        salles.delete()
        return redirect('/')
    
def update_salle(request, salle_id):
    salles = salle.objects.get(id=salle_id)
    
    if request.method == 'POST':
        name = request.POST.get("nom")
        nombre_places = request.POST.get("nb_place")
        
        salles.name = name
        salles.nombre_place = nombre_places
        salles.save()
        return redirect('/')
    
    context = {'salle': salles}
    return render(request, 'salle/salle_update.html', context)

    
    
