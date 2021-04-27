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
    def clean(self):
        username=self.cleaned_data['name']
        memberobj=member.objects.filter(name=username)  
        if len(memberobj)==1:
            if self.instance.id==None:
                raise forms.ValidationError('USER NAME ALREADY EXISTS so please make username unique by adding initials')
            elif memberobj[0].id != self.instance.id :
                raise forms.ValidationError('USER NAME ALREADY EXISTS so please make username unique by adding initials')  
        return self.cleaned_data