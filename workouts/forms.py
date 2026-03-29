from django import forms
from .models import Workout


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['exercise', 'sets', 'reps', 'weight', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control bg-slate-700 border-slate-600 text-slate-100'}),
            'exercise': forms.Select(attrs={'class': 'form-select bg-slate-700 border-slate-600 text-slate-100'}),
            'sets': forms.NumberInput(attrs={'class': 'form-control bg-slate-700 border-slate-600 text-slate-100', 'placeholder': 'e.g. 3'}),
            'reps': forms.NumberInput(attrs={'class': 'form-control bg-slate-700 border-slate-600 text-slate-100', 'placeholder': 'e.g. 10'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control bg-slate-700 border-slate-600 text-slate-100', 'placeholder': 'e.g. 80.5', 'step': '0.5'}),
            'notes': forms.Textarea(attrs={'class': 'form-control bg-slate-700 border-slate-600 text-slate-100', 'rows': 3, 'placeholder': 'Optional notes...'}),
        }
