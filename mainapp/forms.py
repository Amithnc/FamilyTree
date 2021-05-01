from django import forms 
from django.forms import Textarea
from .models import member 
class memberForm(forms.ModelForm):  
    class Meta:  
        model = member  
        fields = ('name','image','password')  
        widgets = {
            'name': Textarea(attrs={'cols': 20, 'rows': 1}),
            'password': forms.PasswordInput(),
        }
    def clean(self):
        username=self.cleaned_data['name']
        memberobj=member.objects.filter(name=username)  
        if len(memberobj)==1:
            if self.instance.id==None:
                raise forms.ValidationError('NAME ALREADY EXISTS so please make FULL NAME unique by adding initials')
            elif memberobj[0].id != self.instance.id :
                raise forms.ValidationError('NAME ALREADY EXISTS so please make FULL NAME unique by adding initials')  
        return self.cleaned_data