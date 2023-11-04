from django.urls import include

from django.contrib import admin

from django.urls import path
from .import views
urlpatterns = [
    path('', views.affiche_matiere_prof),
    #path('ajouter_professeur/',views.ajouter_professeur,name='ajouter_professeur'),
]
