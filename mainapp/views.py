from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from gdstorage.storage import GoogleDriveStorage
gd_storage = GoogleDriveStorage()
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import member
from django.db.models import Q
from .forms import memberForm
from django.contrib.auth.hashers import make_password
option=""
def homepage(request):
    details=member.objects.all()
    return_response={"details":details}
    return render(request,'home.html',return_response)

@login_required(login_url='/login')
def add_member(request):
    user=request.user
    if request.method == "GET":
        global option
        option=request.GET.get('option',None)   
    if request.method == "POST":
        form = memberForm(request.POST or None)
        if form.is_valid():
            details = form.save(commit=False)
            if option=='Partner':
                details.pid=user.id
                details.tag="partner"
                details.password=make_password(details.password)
                details.save()
                messages.success(request, 'Added Successfully go back to see the result ')
                return redirect('/details/')
            elif option=="child":
                user=request.user
                if user.tag=="":
                    criterion1_for_prtner = Q(pid=user.id)
                    criterion2_for_prtner = Q(tag="partner")
                    patrner=member.objects.filter(criterion1_for_prtner & criterion2_for_prtner)
                    details.pid=user.id
                    details.ppid=patrner[0].id
                else:
                    patrner=member.objects.filter(id=user.pid) 
                    details.pid=patrner[0].id
                    details.ppid=user.id
                details.save()
                messages.success(request, 'Added Successfully go back to see the result')
                return redirect('/details/')
    form=memberForm()
    return_response={}
    return_response['form']=form
    return_response['option']="Add "+option+" details"
    return_response['url']='/add-member/'
    return render(request,'addmember.html',return_response)

@login_required(login_url='/login')
def update(request,id):
    instance = get_object_or_404(member,id=id)
    form = memberForm(request.GET or None,instance = instance)
    if request.method == "POST":
        form = memberForm(request.POST  or None,request.FILES,instance = instance)
        if form.is_valid():
            details = form.save(commit=False)
            details.password=make_password(details.password)
            details.save()    
            messages.success(request, 'Updated Successfully go back to see the result')
            return redirect('/details/')
    return_response={}
    return_response['form']=form 
    return_response['option']="Edit Profile:"+instance.name
    return_response['url']='/update/'+str(instance.id)+"/"
    return render(request,'addmember.html',return_response)

@login_required(login_url='/login')
def delete(request,id):
    instance=member.objects.filter(id=id)
    instance.delete()
    messages.success(request, 'Deleted Successfully go back to see the result')
    return redirect('/details/')

@login_required(login_url='/login')
def details(request):
    children=None
    return_response={}
    user=request.user
    root_member=member.objects.filter(name=str(user))
    if root_member[0].tag=="":
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
    else:
        patrner=member.objects.filter(id=root_member[0].pid)   
        if len(patrner)==1:
            criterion1_for_children=Q(ppid=root_member[0].id)
            criterion2_for_children=Q(pid=patrner[0].id)
            children=member.objects.filter(criterion1_for_children & criterion2_for_children)
            return_response['addchildren']=True
    return_response['partner']=patrner
    return_response['children']=children    
    return_response['main_member']=root_member
    return render(request,"details.html",return_response)    

@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    return redirect('/')

