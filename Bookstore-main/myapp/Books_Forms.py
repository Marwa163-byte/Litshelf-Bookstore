from django.forms import ModelForm
from django import forms
from .models import *


class BooksForm(ModelForm):
    class Meta:
       model = Book
       fields = '__all__'
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
        }