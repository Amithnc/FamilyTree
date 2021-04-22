from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from gdstorage.storage import GoogleDriveStorage
gd_storage = GoogleDriveStorage()
from django.contrib.auth.decorators import login_required
from django.contrib import auth

def homepage(request):
    return_response={}
    return render(request,'home.html',return_response)

def addmembers(request):
    return render(request,'addmember.html')

def details(request):
    return render(request,"details.html")    

@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    return render(request,'home.html')
