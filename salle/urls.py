from django.urls import include

from django.contrib import admin
from django.urls import path

from .import views
urlpatterns = [
    
    #path('', views.affiche_salle),
    path('ajouter_salle',views.ajouter_salle,name="ajouter_salle"),
    path('supprimer_salle/<salle_id>',views.supprimer_salle,name="supprimer_salle"),
    path('update_salle/<salle_id>',views.update_salle,name="update_salle"),
    
]
