from django import forms 
from django.forms import Textarea
from .models import member 
class memberForm(forms.ModelForm):  
    class Meta:  
        model = member  
        fields = ('name','image','password')  
        widgets = {
            'name': Textarea(attrs={'cols': 40, 'rows': 1}),
            'password': forms.PasswordInput(),
        }