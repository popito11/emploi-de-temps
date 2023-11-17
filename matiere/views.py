from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Matiere
from .forms import matiereForm




    


def ajouter_matiere(request):
    
    if request.method=='POST':
        nom_mat=request.POST.get("nom")
        code=request.POST.get("code")
        niveau=request.POST.get("niveau")
        nb_seance=request.POST.get("nb_seance")
        nb_eleve=request.POST.get("nb_eleve")
        optionnel=request.POST.get("optionnel")
        opt=False
        if optionnel=="True":
            opt=True
        else:
            opt=False
        matiere=Matiere(nom_matiere=nom_mat,code=code,niveau=niveau,nb_seance=nb_seance,nb_eleve=nb_eleve,optionnel=opt)
        
        matiere.save()
        return redirect('/')
    
    return render(request,'matiere/matiere_save.html')

def supprimer_matiere(request,matiere_id):
    
    matieres=Matiere.objects.get(id=matiere_id)
    if request.method=='POST':
        matieres.delete()
        return redirect('/')
    

def update_matiere(request, matiere_id):
    matieres = Matiere.objects.get(id=matiere_id)
    
    if request.method == 'POST':
        name = request.POST.get("nom")
        code = request.POST.get("code")
        niveau= request.POST.get("niveau")
        nb_seance= request.POST.get("nb_seance")
        nb_eleve= request.POST.get("nb_eleve")
        optionnel=request.POST.get("optionnel")
        print(optionnel)

        if optionnel=="True":
            matieres.optionnel=True
        else:
            matieres.optionnel=False
        
        matieres.nom_matiere = name
        matieres.code = code
        matieres.niveau=niveau
        matieres.nb_seance=nb_seance
        matieres.nb_eleve=nb_eleve
        matieres.save()
        return redirect('/')
    
    context = {'matiere': matieres}
    return render(request, 'matiere/matiere_update.html', context)





