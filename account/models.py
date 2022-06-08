
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# Create your models here.



class CustomAccountManager(BaseUserManager):
    def create_user(self, email, first_name,  last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name= first_name,
            last_name = last_name
        )


        user.set_password(password)
        user.save(using=self._db)
        return user

        
    def create_superuser(self, email, first_name, last_name, password):

        user=  self.create_user(email=email,first_name=first_name, last_name=last_name,  password=password)


        user.is_staff =  True
        user.is_superuser =  True
        user.is_active =  True
        user.is_admin = True
        user.save()
        
        if user.is_superuser is not True:
            raise ValueError('Superuser must be assigned to is_superuser True')

        if user.is_admin is not True:
            raise ValueError('Superuser must be assigned to is_admin True')

        
        if user.is_staff is not True:
            raise ValueError('Superuser must be assigned to is_staff True')
    
    
class User(AbstractBaseUser, PermissionsMixin):
    def avatar_directory_path(instance, filename):
        return '{2}/user_{0}/{1}'.format(instance.id, filename, 'avatar')
        
    id = models.AutoField(primary_key=True)
    email= models.EmailField(_("email address"), max_length=254, unique=True)
    avatar = models.ImageField(upload_to=avatar_directory_path,  blank=True)
    date_of_birth =  models.DateField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default= True)
    is_admin =  models.BooleanField(default=False)
    first_name= models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank= True)
    last_name =  models.CharField(max_length=100)
    date_joined = models.DateTimeField(blank=True, default=timezone.now)
    
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_OTHER = -1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female'), (GENDER_OTHER, 'Other')]
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True)
    
    
    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name

    class Meta:
        db_table=  'users'