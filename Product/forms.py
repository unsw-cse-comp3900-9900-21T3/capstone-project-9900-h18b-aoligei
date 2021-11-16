from .models import Score
from django import forms


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['score']
        widgets = {'score': forms.Textarea(attrs={'cols': 10})}