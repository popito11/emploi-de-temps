from django.shortcuts import render
from django.http import HttpResponse
from .models import MatiereProfesseur
from enseignant.models import Professeur,Horaireprof,Horaire
from matiere.models import Matiere
from salle.models import salle 

import random


def tri_fusion_salles(tab):
    if len(tab) <= 1:
        return tab

    milieu = len(tab) // 2
    gauche = tab[:milieu]
    droite = tab[milieu:]

    gauche = tri_fusion_salles(gauche)
    droite = tri_fusion_salles(droite)

    return fusion_salles(gauche, droite)

def fusion_salles(gauche, droite):
    resultat = []
    i = j = 0

    while i < len(gauche) and j < len(droite):
        if gauche[i].nombre_place < droite[j].nombre_place:
            resultat.append(gauche[i])
            i += 1
        else:
            resultat.append(droite[j])
            j += 1

    while i < len(gauche):
        resultat.append(gauche[i])
        i += 1

    while j < len(droite):
        resultat.append(droite[j])
        j += 1

    return resultat


def get_permutation(tab):
    random.shuffle(tab)
    return tab
           
def generer_emploi(request):

    Professeurs=Professeur.objects.all()
    Matieres=Matiere.objects.all()
    salles=salle.objects.all()
    MatiereProfesseurs=MatiereProfesseur.objects.all()
    Horaireprofs=Horaireprof.objects.all()
    
    salles = tri_fusion_salles(salles)

    # les lignes ici représentent les plages horaire ;
    # les colonnes représentent les jours de la semaine ;
    # le tableau dans chaque case répresentent les profs ;

    emploi_temps_prof = [[[], [], [], [], []],
                         [[], [], [], [], []],
                         [[], [], [], [], []],
                         [[], [], [], [], []],
                         [[], [], [], [], []]]
    
    emploi_temps_salle = [[[], [], [], [], []],
                          [[], [], [], [], []],
                          [[], [], [], [], []],
                          [[], [], [], [], []],
                          [[], [], [], [], []]]
    
    emploi_temps_niveau= [[[], [], [], [], []],
                          [[], [], [], [], []],
                          [[], [], [], [], []],
                          [[], [], [], [], []],
                          [[], [], [], [], []]]
    
    nbseance_prof_emploi=[]
    matieres_ops=[]
    matiere_ob=[]
    
    for matiere in Matieres:
        if matiere.optionnel==True:
            matieres_ops.append(matiere)
        else:
            matiere_ob.append(matiere)
    
    Matieres=[]

    for matiere in matieres_ops:
        Matieres.append(matiere)
    for matiere in matiere_ob:
        Matieres.append(matiere)

    #print(Matieres)
    #parcour des matiere afin d'extraire les niveaux pour les mettre dans un tableau niveaux 
    niveaux=[0]
    for matiere in Matieres:
        trouve=0
        for niv in niveaux:
            if matiere.niveau == niv:
                trouve=1
        if trouve==0:
            niveaux.append(matiere.niveau)
    niveaux.pop(0)
    #print(niveaux)


    #creation d'un matrice niveau mappé avec le niveau a laquelle appartien la matrice . cela nous permet d'avoir l'emploi de temps d'un niveau
    niveau=[]
             
    for niv in niveaux:
        niveau.append([niv,[[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]]])
    
    #print(niveau[2][1])

    
    #recuperation nombre de prof et de salle 
    nb_prof=len(Professeurs)
    nb_salle=len(salles)


    #remplissage des cube representant l'emploi de temps principale (emploi_temps_prof) , l'emploi de temps d'etat des salle et des niveaux .
    #l'etat permet de savoir si une ressource est libre a une plage horaire donnee ou pas
    #l'emploi de temps principale est mappé avec le professeur ; celui des salle avec la salle ...
    for plage in range(5):
        for jour in range(5):
            for nb in range(nb_prof):
                emploi_temps_prof[plage][jour].append([Professeurs[nb],0,0])
                if plage==0 and jour==0:
                    nbseance_prof_emploi.append([Professeurs[nb],0])

    for plage in range(5):
        for jour in range(5):
            for nb in range(nb_salle):
                emploi_temps_salle[plage][jour].append([salles[nb],0])

    for plage in range(5):
        for jour in range(5):
            for nb in range(len(niveaux)):
                emploi_temps_niveau[plage][jour].append([niveaux[nb],0]) 
                """le 1er 0 me permet de savoir si une il y'a une matiere d'un niveau donnee dans une plage horaire
                le 2eme 0 me permet de savoir si parmi les matieres presentes il y'a une qui est obligatoire 
                si c'est le cas (emploi_temps_niveau[plage][jour][1]==2) alors on n'y ajoute plus de matiere du 
                meme niveau dans cette plage , si ce n'est pas le cas (ie il n'ya que des matiere optionnelle ,
                emploi_temps_niveau[plage][jour][1]==1) alors on peut ajouter des matiere optionnelle suplementaire 
                du meme niveau . emploi_temps_niveau[plage][jour][1]==0 : il n'y a pas de matiere de ce niveau dans 
                la plage horaire"""
    
    
    #ici on cherche a modifie l'etat d'un prof sur l'emploi de temps en fonction de ses plage horaire occupé
    #on a mis 1 au niveau de la case reservé au matiere , partout ou il est occupé (emploi_temps_prof[plage][jour][nb][1]=1)
    for horaire in Horaireprofs:
        for plage in range(5):
            if int(horaire.Horaire.plage)==plage+1:
                for jour in range(5):
                    if (horaire.jour=="lundi" and jour==0) or (horaire.jour=="mardi" and jour==1 ) or (horaire.jour=="mercredi" and jour==2 ) or (horaire.jour=="jeudi" and jour==3) or (horaire.jour=="vendredi" and jour==4):
                        for nb in range(nb_prof):
                            if horaire.Professeur==emploi_temps_prof[plage][jour][nb][0] :
                                emploi_temps_prof[plage][jour][nb][1]=1


    #print(emploi_temps_prof)               
    
    compteur=0 # variable qui permet de propagé les breaks une fois une matiere mis dans l'emploi de temps
    
    #cette boucle for principale est celle utilisé pour mettre les matiere avec les salle correspondant dans l'emploi de temps
    for matiere in Matieres :
        compteur=0        
        for i in range(matiere.nb_seance):
            compteur=0
            for mat_prof in MatiereProfesseurs:
                if compteur==1:
                    break
                if mat_prof.Matiere==matiere:

                    #choix de la salle correspondant a la matiere
                    for sal in salles:
                        if matiere.nb_eleve <= sal.nombre_place : 
                            salle_courant=sal
                            break
                    
                    #ici je regarde l'indice (comps) ou se trouve la salle dans un des tableau de l'emploi de temps ici j'ai pris l'exemple de [1][1]
                    comps=0                    
                    for sall in emploi_temps_salle[1][1]:
                        if sall[0]==salle_courant:
                            break
                        comps=comps+1
                    
                    #ici je regarde l'indice (compn) ou se trouve le niveau dans un des tableau de l'emploi de temps ici j'ai pris l'exemple de [1][1]
                    compn=0                    
                    for nive in emploi_temps_niveau[1][1]:
                        if nive[0]==matiere.niveau:
                            break
                        compn=compn+1

                    #parcour de la matrice pour y mettre l'emploi de la matiere et la salle dans une plage 
                    for plage in range(5):
                        if compteur==1:
                            break
                        for jour in range(5):
                            if compteur==1:
                                break
                            for nb in range(nb_prof):
                                # on verifie si le professeur correspond bien au professeur de la plage ; si ce professeur est libre a cette plage ; 
                                # si a une meme plage horaire on ne fait pas cour dans la meme salle ; si a une meme plage horaire on ne fait pas deux matieres obligatoires du meme niveau
                                # a noter la verification pour la salle et pour le niveau ont etes implementé de la meme facon 
                                   
                                if mat_prof.Professeur==emploi_temps_prof[plage][jour][nb][0] and emploi_temps_prof[plage][jour][nb][1]==0  and (emploi_temps_niveau[plage][jour][compn-1][1]==0 or (emploi_temps_niveau[plage][jour][compn-1][1]==1 and matiere.optionnel==True)):
                                    
                                    emploi_temps_prof[plage][jour][nb][1]=matiere
                                    emploi_temps_prof[plage][jour][nb][2]=salle_courant
                                    compteur=1
                                    
                                    #print (matiere.code)  
                                    #mise a jour du nombre de seance que le prof fait par semaine
                                    nbseance_prof_emploi[nb][1] +=1

                                    #modification d'etat d'une salle et d'un niveau
                                    emploi_temps_salle[plage][jour][comps-1][1]=1
                                    if  matiere.optionnel==False:
                                        emploi_temps_niveau[plage][jour][compn-1][1]=2
                                    else:
                                        emploi_temps_niveau[plage][jour][compn-1][1]=1

                                    break
                    
    

    
    
    nb_iter=0
    compteur1=0
    #print(nbseance_prof_emploi)
    matiere_emploi_prof_courant=[]
    for nbseance_prof in nbseance_prof_emploi:
        nb_iter=0
        while nbseance_prof[1]>nbseance_prof[0].nombre_seance:
            print("***********************************************************************************")
            print("courant : ", matiere_emploi_prof_courant)
            matiere_emploi_prof_courants=get_permutation(matiere_emploi_prof_courant)
            print("permuter",matiere_emploi_prof_courants)
            plage_seance=0
            for plage in range(5):
                for jour in range(5):
                    for nb in range(nb_prof):
                        if emploi_temps_prof[plage][jour][nb][0]== nbseance_prof[0] and emploi_temps_prof[plage][jour][nb][1]!=1 and emploi_temps_prof[plage][jour][nb][1]!=0:
                            if nb_iter !=0:
                                print("-------------------------------------------------------------------------")
                                emploi_temps_prof[plage][jour][nb][1]=matiere_emploi_prof_courants[plage_seance][0]
                                print(matiere_emploi_prof_courants[plage_seance][0])
                                emploi_temps_prof[plage][jour][nb][2]=matiere_emploi_prof_courants[plage_seance][1]
                                print(matiere_emploi_prof_courants[plage_seance][1])
                                print("-------------------------------------------------------------------------")
                                plage_seance+=1

            nb_iter+=1
            if nb_iter>75:
                break
            compteur1=0
            for plage in range(5):
                if compteur1==1:
                    break
                for jour in range(5):
                    if compteur1==1:
                        break
                    for nb in range(nb_prof):
                        if compteur1==1:
                            break
                        if emploi_temps_prof[plage][jour][nb][0]== nbseance_prof[0]  and emploi_temps_prof[plage][jour][nb][1]!=1 and emploi_temps_prof[plage][jour][nb][1]!=0:
                            
                            #print("plage : ",plage,"jour : ",jour)

                            if [emploi_temps_prof[plage][jour][nb][1],emploi_temps_prof[plage][jour][nb][2]] in matiere_emploi_prof_courant:
                                ignorer=1
                            else :
                                matiere_emploi_prof_courant.append([emploi_temps_prof[plage][jour][nb][1],emploi_temps_prof[plage][jour][nb][2]])
                                

                            for mat_prof in MatiereProfesseurs:
                                if compteur1==1:
                                    break
                                
                                if mat_prof.Professeur!=nbseance_prof[0] and mat_prof.Matiere==emploi_temps_prof[plage][jour][nb][1]  :
                                    

                                    for nb1 in range(nb_prof):
                                        """
                                        print("--------------------------------------")
                                        print(emploi_temps_prof[plage][jour][nb1][0])
                                        print(mat_prof.Professeur)
                                        print("******************************************************")
                                        print(emploi_temps_prof[plage][jour][nb1][1])
                                        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")
                                        print(nbseance_prof_emploi[nb1][1])
                                        """
                                        if emploi_temps_prof[plage][jour][nb1][0]==mat_prof.Professeur:
                                            #print("",nbseance_prof[0] ,"---", emploi_temps_prof[plage][jour][nb1][0],"---mat--- ",mat_prof.Professeur,"---matiere---", emploi_temps_prof[plage][jour][nb1][1]," plage ",plage," jour ",jour)
                                            print("")
                                        if emploi_temps_prof[plage][jour][nb1][0]==mat_prof.Professeur and emploi_temps_prof[plage][jour][nb1][1]==0 :
                                            
                                            print(nbseance_prof[0] ,"---", emploi_temps_prof[plage][jour][nb1][0])

                                            emploi_temps_prof[plage][jour][nb1][1]=mat_prof.Matiere
                                            emploi_temps_prof[plage][jour][nb1][2]=emploi_temps_prof[plage][jour][nb][2]

                                            emploi_temps_prof[plage][jour][nb][2]=0
                                            emploi_temps_prof[plage][jour][nb][1]=0

                                            nbseance_prof_emploi[nb][1]-=1
                                            nbseance_prof_emploi[nb1][1]+=1
                                            
                                            compteur1=1
                                            break


    #print(nb_iter)
    #print(nbseance_prof_emploi)
    #separation de l'emploi de temps en fonction de differents niveaux en mettant chaque noeud (prof;matiere;salle) dans la matrice niveau correspondant
    for nive in niveaux:
        for plage in range(5):
            for jour in range(5):
                for nb in range(nb_prof):
                    #on verifie si une matiere a ete stoker dans le noeud ; si le prof n'etait pas occupé a cette plage la (horaireprof);si le niveau de la matiere correspond bien
                    if emploi_temps_prof[plage][jour][nb][1]!=0 and emploi_temps_prof[plage][jour][nb][1]!=1 and emploi_temps_prof[plage][jour][nb][1].niveau==nive: 
                        for i in range(len(niveau)) :
                            if nive == niveau[i][0]:
                                niveau[i][1][plage][jour].append(emploi_temps_prof[plage][jour][nb])
                                
                                break
                    
    #ici on reuini les emplois de temps de chaque niveau pour les mettre dans un tableau (pour forme un cube ie dim =3) 
    
    emploi_temps=[]
    for nive in niveau:
        emploi_temps.append(nive[1])

    #print(emploi_temps)
    print("nb_iter :", nb_iter)
    context={'emploi_temps':emploi_temps,'iter':nb_iter}
    return render(request,'emploi_temps.html',context)
