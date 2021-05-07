from django import forms 
from django.forms import Textarea
from .models import member 
class memberForm(forms.ModelForm):  
    class Meta:  
        model = member  
        fields = ('name','image','password')  
        widgets = {
            'name': forms.TextInput(),
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
        imagefile=self.cleaned_data['image']    
        if imagefile:    
            file_extension=str(imagefile).split('.')
            if file_extension[1].lower()!= 'jpg' and file_extension[1].lower()!='png' and file_extension[1].lower()!= 'jpeg':
                raise forms.ValidationError('FILE NOT SUPPORTED only jpg or png or jpeg formets are allowed')
        return self.cleaned_data