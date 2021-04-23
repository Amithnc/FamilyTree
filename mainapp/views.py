from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from gdstorage.storage import GoogleDriveStorage
gd_storage = GoogleDriveStorage()
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import member
from django.db.models import Q

def homepage(request):
    return_response={}
    return render(request,'home.html',return_response)

def addmembers(request):
    return render(request,'addmember.html')

@login_required(login_url='/login')
def details(request):
    children=None
    return_response={}
    user=request.user
    root_member=member.objects.filter(name=str(user))
    criterion1_for_prtner = Q(pid=root_member[0].id)
    criterion2_for_prtner = Q(tag="partner")
    patrner=member.objects.filter(criterion1_for_prtner & criterion2_for_prtner)
    if len(patrner)==0:
        return_response['addpatner']=True
    elif len(patrner)==1:
        criterion1_for_children=Q(pid=root_member[0].id)
        criterion2_for_children=Q(ppid=patrner[0].id)
        children=member.objects.filter(criterion1_for_children & criterion2_for_children)
        return_response['addchildren']=True  
    return_response['partner']=patrner
    return_response['children']=children    
    return_response['main_member']=root_member[0].name 
    return render(request,"details.html",return_response)    

@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    return render(request,'home.html')
