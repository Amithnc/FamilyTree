from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from gdstorage.storage import GoogleDriveStorage
gd_storage = GoogleDriveStorage()

class MymemberManager(BaseUserManager):
    def create_user(self,name,pid,ppid,password=None):
        if not name:
            raise ValueError("USERS SHOULD HAVE NAME")
        if not pid:
            raise ValueError("USERS SHOULD HAVE PID")
        if not ppid:
            raise ValueError("USERS SHOULD HAVE PPID")

        user= self.model(
            name=name,
            pid=pid,
            ppid=ppid,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,name,pid,ppid,password):
        user= self.create_user(
            name=name,
            pid=pid,
            ppid=ppid,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class member(AbstractBaseUser):
    name                =models.CharField(max_length=50,default='',unique=True,verbose_name='FULL NAME')
    pid                 =models.IntegerField()
    ppid                =models.IntegerField(default=-1)
    image               =models.ImageField(upload_to='images/',default='',blank=True)
    tag                 =models.CharField(max_length=50,default='',blank=True)
    url                 =models.CharField(max_length=80,default='',blank=True)
    date_joined         =models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login          =models.DateTimeField(verbose_name='last login',auto_now=True)
    is_admin            =models.BooleanField(default=False)
    is_active           =models.BooleanField(default=True)
    is_staff            =models.BooleanField(default=False)
    is_superuser        =models.BooleanField(default=False)
    
    USERNAME_FIELD='name'
    REQUIRED_FIELDS=['pid','ppid',]

    objects=MymemberManager()

    def __str__(self):
         return self.name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name_plural = "FAMILY-DATA"     