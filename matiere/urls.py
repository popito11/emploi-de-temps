from django.urls import include

from django.contrib import admin
from django.urls import path

from .import views
urlpatterns = [
    #path('', views.home),
    #path('',views.HOME),
    path('ajouter_matiere',views.ajouter_matiere,name="ajouter_matiere"),
    path('supprimer_matiere/<matiere_id>',views.supprimer_matiere,name="supprimer_matiere"),
    path('update_matiere/<matiere_id>',views.update_matiere,name="update_matiere"),
    #path('',views.affiche_matiere),
    
]
