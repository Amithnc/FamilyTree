from .models import member
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from gdstorage.storage import GoogleDriveStorage
gd_storage = GoogleDriveStorage()

@receiver(post_save, sender=member)
def update_url_instance(sender, instance, created, **kwargs):
    url=""
    memberobj=member.objects.filter(id=instance.id)
    if instance.image !="" and instance.image != None  and memberobj[0].image !="" and memberobj[0].image != None :
        try:
            path=gd_storage.url(str(instance.image))
            splitted_url=path.split('&')
            splitted_url[1]='export=view'
            url="&".join(splitted_url)
            member.objects.filter(id=instance.id).update(url=url)
        except:
            pass
    if instance.image =="" or memberobj[0].image=="" or memberobj[0].image==None and instance.url !="":
        member.objects.filter(id=instance.id).update(url="")
    pswd=str(instance.password)    
    # if pswd[]

