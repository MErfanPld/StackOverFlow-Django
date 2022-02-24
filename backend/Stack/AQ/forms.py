from django import forms
from .models import Answer


class AnswerCreateForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }


class AnswerReplyForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control'})
        }

