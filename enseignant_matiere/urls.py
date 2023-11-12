from django.urls import include

from django.contrib import admin

from django.urls import path
from .import views
urlpatterns = [
    path('generer',views.generer_emploi,name="generer_emploi"),
    path('emploi_temps',views.emploi_de_temps),
    #path('ajouter_professeur/',views.ajouter_professeur,name='ajouter_professeur'),
]
