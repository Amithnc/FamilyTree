from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from gdstorage.storage import GoogleDriveStorage
gd_storage = GoogleDriveStorage()

def homepage(request):
    path=gd_storage.url('Amith_N_C_1')
    splitted_url=path.split('&')
    splitted_url[1]='export=view'
    url="&".join(splitted_url)
    return_response={}
    return_response['url']=url
    return render(request,'home.html',return_response)
