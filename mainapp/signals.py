from .models import member
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from gdstorage.storage import GoogleDriveStorage
gd_storage = GoogleDriveStorage()

flag=0

@receiver(post_save, sender=member)
def update_url_instance(sender, instance, created, **kwargs):
    url=""
    global flag
    if instance.image !="" and flag==0:
        flag=1
        path=gd_storage.url(str(instance.image))
        print(path)
        splitted_url=path.split('&')
        splitted_url[1]='export=view'
        url="&".join(splitted_url)
        member.objects.filter(id=instance.id).update(url=url)
    if instance.image =="" and instance.url !="":
        member.objects.filter(id=instance.id).update(url="")
    pswd=str(instance.password)    
    # if pswd[]

