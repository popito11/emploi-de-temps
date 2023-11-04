from django.forms import ModelForm
from .models import Matiere

class matiereForm(ModelForm):
    class Meta:
        model=Matiere
        fields='__all__'