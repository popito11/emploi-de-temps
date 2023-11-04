from django.urls import include
from .import views
from django.contrib import admin
from django.urls import path

urlpatterns = [   
    path('', views.HOME),
    #path('', views.home,name='accueil'),
    path('ajouter_professeur/',views.ajouter_professeur,name='ajouter_professeur'),
    path('update_professeur/<professeur_id>',views.update_professeur,name="update_professeur"),
    path('supprimer_professeur/<professeur_id>',views.supprimer_professeur,name='supprimer_professeur'),
    path('read_professeur/<professeur_id>',views.read_professeur,name="read_professeur"),

   
]