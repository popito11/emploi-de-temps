from django.shortcuts import render,redirect
from .models import Professeur,Horaireprof,Horaire
from matiere.models import Matiere
from salle.models import salle 
from enseignant_matiere.models import MatiereProfesseur


from django.http import HttpResponse
from .forms import enseignantForm


def HOME(request):
    enseignants=Professeur.objects.all()
    horaire=Horaireprof.objects.all()
    matiere=Matiere.objects.all()
    Salle=salle.objects.all()
    context={'Enseignants':enseignants,'Horaires':horaire,'salles':Salle,'matieres':matiere}
    return render(request,'base.html',context)

# Create your views here.

def ajouter_professeur(request):
    list_matiere = Matiere.objects.all()
    list_horaire = Horaire.objects.all()
    if request.method == 'POST':
        nom_prof = request.POST.get("nom")
        telephone = request.POST.get("telephone")
        email = request.POST.get("email")
        professeur = Professeur(nom_prof=nom_prof, email=email, telephone=telephone)
        professeur.save()

        liste=request.POST.getlist("nomf")
        for iden in liste:
            for mat in list_matiere: 
                if str(mat.id)==iden:
                    matiere_p=MatiereProfesseur.objects.create(Professeur=professeur, Matiere=mat)
                    matiere_p.save()

        
        
        p1j1=request.POST.get("case-1-1")
        p1j2=request.POST.get("case-1-2")
        p1j3=request.POST.get("case-1-3")
        p1j4=request.POST.get("case-1-4")
        p1j5=request.POST.get("case-1-5")
        p2j1=request.POST.get("case-2-1")
        p2j2=request.POST.get("case-2-2")
        p2j3=request.POST.get("case-2-3")
        p2j4=request.POST.get("case-2-4")
        p2j5=request.POST.get("case-2-5")
        p3j1=request.POST.get("case-3-1")
        p3j2=request.POST.get("case-3-2")
        p3j3=request.POST.get("case-3-3")
        p3j4=request.POST.get("case-3-4")
        p3j5=request.POST.get("case-3-5")
        p4j1=request.POST.get("case-4-1")
        p4j2=request.POST.get("case-4-2")
        p4j3=request.POST.get("case-4-3")
        p4j4=request.POST.get("case-4-4")
        p4j5=request.POST.get("case-4-5")
        p5j1=request.POST.get("case-5-1")
        p5j2=request.POST.get("case-5-2")
        p5j3=request.POST.get("case-5-3")
        p5j4=request.POST.get("case-5-4")
        p5j5=request.POST.get("case-5-5")

        tableau=[[p1j1,p1j2,p1j3,p1j4,p1j5],[p2j1,p2j2,p2j3,p2j4,p2j5],[p3j1,p3j2,p3j3,p3j4,p3j5],[p4j1,p4j2,p4j3,p4j4,p4j5],[p5j1,p5j2,p5j3,p5j4,p5j5]]
        for tab in tableau :
            for tib in tab:
                print(tib)
        for i in range(5):
            for j in range(5):
                if j == 0 and tableau[i][j] =="true":
                    h1=Horaireprof.objects.create(Professeur=professeur, Horaire=list_horaire[i], jour="lundi")
                    h1.save()
                if j == 1 and tableau[i][j] == "true":
                    h2=Horaireprof.objects.create(Professeur=professeur, Horaire=list_horaire[i], jour="mardi")
                    h2.save()
                if j == 2 and tableau[i][j] == "true":
                    h3=Horaireprof.objects.create(Professeur=professeur, Horaire=list_horaire[i], jour="mercredi")
                    h3.save()
                if j == 3 and tableau[i][j] == "true":
                    h4=Horaireprof.objects.create(Professeur=professeur, Horaire=list_horaire[i], jour="jeudi")
                    h4.save()
                if j == 4 and tableau[i][j] == "true":
                    h5=Horaireprof.objects.create(Professeur=professeur, Horaire=list_horaire[i], jour="vendredi")
                    h5.save()
        return redirect('/')

    context = {'matieres': list_matiere}   
    return render(request, 'enseignant/professeur_save.html', context)


def modifier_enseignant(request,enseignant_id):
    enseignant=Professeur.objects.get(id=enseignant_id)
    form=enseignantForm(instance=enseignant)
    if request.method=='POST':
        form=enseignantForm(request.POST,instance=enseignant)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'formu':form}
    return render(request,'enseignant/ajout_enseignant.html',context)


def supprimer_professeur(request,professeur_id):
    
    professeurs=Professeur.objects.get(id=professeur_id)
    if request.method=='POST':
        professeurs.delete()
        return redirect('/')



def update_professeur(request, professeur_id):
    professeurs = Professeur.objects.get(id=professeur_id)
    matieres=Matiere.objects.all()
    matiere_profs=MatiereProfesseur.objects.all()
    horaireprof=Horaireprof.objects.all()
    list_horaire = Horaire.objects.all()

    if request.method == 'POST':

        #---------------------------------------------------------------------------#
        name = request.POST.get("nom")
        telephone = request.POST.get("telephone")
        email = request.POST.get("email")
        
        professeurs.nom_prof = name
        professeurs.telephone = telephone
        professeurs.email = email



        liste=request.POST.getlist("nomf")
        for matprof in matiere_profs:
            if matprof.Professeur==professeurs:
                print("-------------------------------------------------------------------------------------")
                print(matprof)
                matprof.delete()


        for hprof in horaireprof:
            if hprof.Professeur==professeurs:
                hprof.delete()

        professeurs.save()

        #---------------------------------------------------------------------------#
        

        for iden in liste:
            for mat in matieres: 
                if str(mat.id)==iden:
                    matiere_p=MatiereProfesseur.objects.create(Professeur=professeurs, Matiere=mat)
                    matiere_p.save()

        #----------------------------------------------------------------------------------#
        


        p1j1=request.POST.get("case-1-1")
        p1j2=request.POST.get("case-1-2")
        p1j3=request.POST.get("case-1-3")
        p1j4=request.POST.get("case-1-4")
        p1j5=request.POST.get("case-1-5")
        p2j1=request.POST.get("case-2-1")
        p2j2=request.POST.get("case-2-2")
        p2j3=request.POST.get("case-2-3")
        p2j4=request.POST.get("case-2-4")
        p2j5=request.POST.get("case-2-5")
        p3j1=request.POST.get("case-3-1")
        p3j2=request.POST.get("case-3-2")
        p3j3=request.POST.get("case-3-3")
        p3j4=request.POST.get("case-3-4")
        p3j5=request.POST.get("case-3-5")
        p4j1=request.POST.get("case-4-1")
        p4j2=request.POST.get("case-4-2")
        p4j3=request.POST.get("case-4-3")
        p4j4=request.POST.get("case-4-4")
        p4j5=request.POST.get("case-4-5")
        p5j1=request.POST.get("case-5-1")
        p5j2=request.POST.get("case-5-2")
        p5j3=request.POST.get("case-5-3")
        p5j4=request.POST.get("case-5-4")
        p5j5=request.POST.get("case-5-5")

        tableau=[[p1j1,p1j2,p1j3,p1j4,p1j5],[p2j1,p2j2,p2j3,p2j4,p2j5],[p3j1,p3j2,p3j3,p3j4,p3j5],[p4j1,p4j2,p4j3,p4j4,p4j5],[p5j1,p5j2,p5j3,p5j4,p5j5]]
        
        for i in range(5):
            for j in range(5):
                if j == 0 and tableau[i][j] =="true":
                    h1=Horaireprof.objects.create(Professeur=professeurs, Horaire=list_horaire[i], jour="lundi")
                    h1.save()
                if j == 1 and tableau[i][j] == "true":
                    h2=Horaireprof.objects.create(Professeur=professeurs, Horaire=list_horaire[i], jour="mardi")
                    h2.save()
                if j == 2 and tableau[i][j] == "true":
                    h3=Horaireprof.objects.create(Professeur=professeurs, Horaire=list_horaire[i], jour="mercredi")
                    h3.save()
                if j == 3 and tableau[i][j] == "true":
                    h4=Horaireprof.objects.create(Professeur=professeurs, Horaire=list_horaire[i], jour="jeudi")
                    h4.save()
                if j == 4 and tableau[i][j] == "true":
                    h5=Horaireprof.objects.create(Professeur=professeurs, Horaire=list_horaire[i], jour="vendredi")
                    h5.save()

        return redirect('/')
    
    context = {'professeur': professeurs,'matieres':matieres}
    return render(request, 'enseignant/professeur_update.html', context)


def read_professeur(request, professeur_id):
    professeurs = Professeur.objects.get(id=professeur_id)
    matiere_profs=MatiereProfesseur.objects.all()
    horaireprof=Horaireprof.objects.all()
    list_horaire = Horaire.objects.all()

    listMatiereProf=[]
    listHoraireProf=[]

    for listh in horaireprof:
        if listh.Professeur==professeurs:
            listHoraireProf.append(listh)

    for matprof in matiere_profs:
            if matprof.Professeur==professeurs:
                listMatiereProf.append(matprof.Matiere)

    Matrice=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]


    for hprof in listHoraireProf:
        if hprof.Horaire.plage=="1" and hprof.jour=="lundi":
            Matrice[0][0]=1
        if hprof.Horaire.plage=="1" and hprof.jour=="mardi":
            Matrice[0][1]=1   
        if hprof.Horaire.plage=="1" and hprof.jour=="mercredi":
            Matrice[0][2]=1 
        if hprof.Horaire.plage=="1" and hprof.jour=="jeudi":
            Matrice[0][3]=1 
        if hprof.Horaire.plage=="1" and hprof.jour=="vendredi":
            Matrice[0][4]=1 
        
        #------------------------------------------------------------#

        if hprof.Horaire.plage=="2" and hprof.jour=="lundi":
            Matrice[1][0]=1
        if hprof.Horaire.plage=="2" and hprof.jour=="mardi":
            Matrice[1][1]=1   
        if hprof.Horaire.plage=="2" and hprof.jour=="mercredi":
            Matrice[1][2]=1 
        if hprof.Horaire.plage=="2" and hprof.jour=="jeudi":
            Matrice[1][3]=1 
        if hprof.Horaire.plage=="2" and hprof.jour=="vendredi":
            Matrice[1][4]=1    
        #------------------------------------------------------------#

        if hprof.Horaire.plage=="3" and hprof.jour=="lundi":
            Matrice[2][0]=1
        if hprof.Horaire.plage=="3" and hprof.jour=="mardi":
            Matrice[2][1]=1   
        if hprof.Horaire.plage=="3" and hprof.jour=="mercredi":
            Matrice[2][2]=1 
        if hprof.Horaire.plage=="3" and hprof.jour=="jeudi":
            Matrice[2][3]=1 
        if hprof.Horaire.plage=="3" and hprof.jour=="vendredi":
            Matrice[2][4]=1    

        #------------------------------------------------------------#

        if hprof.Horaire.plage=="4" and hprof.jour=="lundi":
            Matrice[3][0]=1
        if hprof.Horaire.plage=="4" and hprof.jour=="mardi":
            Matrice[3][1]=1   
        if hprof.Horaire.plage=="4" and hprof.jour=="mercredi":
            Matrice[3][2]=1 
        if hprof.Horaire.plage=="4" and hprof.jour=="jeudi":
            Matrice[3][3]=1 
        if hprof.Horaire.plage=="4" and hprof.jour=="vendredi":
            Matrice[3][4]=1

        #------------------------------------------------------------#

        if hprof.Horaire.plage=="5" and hprof.jour=="lundi":
            Matrice[4][0]=1
        if hprof.Horaire.plage=="5" and hprof.jour=="mardi":
            Matrice[4][1]=1   
        if hprof.Horaire.plage=="5" and hprof.jour=="mercredi":
            Matrice[4][2]=1 
        if hprof.Horaire.plage=="5" and hprof.jour=="jeudi":
            Matrice[4][3]=1 
        if hprof.Horaire.plage=="5" and hprof.jour=="vendredi":
            Matrice[4][4]=1

    context = {'professeur': professeurs,'matieres':listMatiereProf,'matrice':Matrice,'horaire':list_horaire}
    return render(request, 'enseignant/professeur_read.html', context)
    