from django.forms import ModelForm
from .models import Professeur

class enseignantForm(ModelForm):
    class Meta:
        model=Professeur
        fields='__all__'