from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from .models import member
from django.db.models import Q
from .forms import memberForm
from django.contrib.auth.hashers import make_password
option=""
def homepage(request):
    # # gd_storage.delete('filename') #- to delete file
    # a,b=gd_storage.listdir("googlefiles") 
    # print(b)
    details=member.objects.all()
    return_response={"details":details}
    return render(request,'home.html',return_response)

@login_required(login_url='/login')
def add_member(request):
    user=request.user
    if request.method == "GET":
        global option
        option=request.GET.get('option',None)
        form=memberForm()
    if request.method == "POST":
        form = memberForm(request.POST or None,request.FILES)
        if form.is_valid():
            details = form.save(commit=False)
            if option=='Partner':
                details.pid=user.id
                details.tag="partner"
                details.password=make_password("Nidaghatta")
                details.save()
                messages.success(request, '✔️ Added Successfully go back to see the result')
                return JsonResponse({'meassage':'success'})
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
                details.password=make_password("Nidaghatta")
                details.save()
                messages.success(request, '✔️ Added Successfully go back to see the result')
                return JsonResponse({'meassage':'success'},status=200)
        else:
            form.errors.as_data()
            for e in form.errors['__all__'].as_data():
                temp=str(e)
                error=temp[2:-2]    
            return JsonResponse({"error": error}, status=400)
    return_response={}
    return_response['form']=form
    return_response['option']="Add your "+option+" details"
    return_response['url']='/add-member/'
    return_response['title']='ADD  '+option
    return render(request,'addmember.html',return_response)

@login_required(login_url='/login')
def update(request,id):
    user=request.user
    id_s=[user.id]
    try:
        if user.tag=="":
            partner=get_object_or_404(member,Q(pid=user.id) & Q(tag="partner"))
        else:
            partner=get_object_or_404(member,id=user.pid)
        id_s.append(partner.id)
        c1=Q(pid=user.id)
        c2=Q(ppid=partner.id)
        c3=Q(pid=partner.id)
        c4=Q(ppid=user.id)
        children=member.objects.filter((c1 & c2) | (c3 & c4) )
        for child in children:
            id_s.append(child.id)
    except Exception as e:
        print(e)
    if id not in id_s:
        messages.error(request, 'You can only edit your family details')
        return redirect('/details/')
    instance = get_object_or_404(member,id=id)
    form = memberForm(request.GET or None,instance = instance)
    if request.method == "POST":
        form = memberForm(request.POST  or None,request.FILES,instance = instance)
        if form.is_valid():
            details = form.save(commit=False)
            url=details.url
            if url=="delete image":
                details.image=None
            details.password=make_password("Nidaghatta")
            details.save()
            messages.success(request, '✔️ Updated Successfully go back to see the result')
            return JsonResponse({'meassage':'success'},status=200)
        else:   
            form.errors.as_data() 
            for e in form.errors['__all__'].as_data():
                temp=str(e)
                error=temp[2:-2]    
            return JsonResponse({"error": error}, status=400)     
    return_response={}
    return_response['form']=form
    return_response['option']="Edit Profile:"+instance.name
    return_response['url']='/update/'+str(instance.id)+"/"
    return_response['title']='Update Profile- '+str(instance.name)
    return render(request,'addmember.html',return_response)

@login_required(login_url='/login')
def delete(request):
    id=request.POST.get('id_to_delete',None)
    partner=member.objects.filter(id=id)
    children=member.objects.filter(ppid=partner[0].id)
    partner.delete()
    for obj in children:
        obj.delete()
    messages.success(request, '✔️ Deleted Successfully go back to see the result')
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
    if user.tag == "partner":
        return_response['partner_delete']=True
    return_response['partner']=patrner
    return_response['children']=children
    return_response['main_member']=root_member
    return render(request,"details.html",return_response)

@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    messages.success(request, '✔️ Logged Out Successfully Thanks for your time :) ')
    return redirect('/')


