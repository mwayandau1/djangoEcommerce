from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def createUser(self, first_name, last_name, username, email, password=None):
        if not username:
            raise ValueError("User must have a user name to continue!")
        if not email:
            raise ValueError("User must have email address to continue!")
        
        user = self.model(
            email= self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save(using= self._db)
        return user
    
    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.createUser(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True
        user.save(using = self._db)
        return user
    

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=40, unique=True)
    phone = models.CharField(max_length=11, blank=True)


    last_login = models.DateTimeField(auto_now_add=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def full_name(self):
        return f'{self.first_name + " "+ self.last_name}'

    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    address_line_1 = models.CharField(max_length=100, blank=True)
    address_line_2 = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to='profile/')
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.user.first_name
    
    def full_name(self):
        return f'{self.address_line_1} + " " +{self.address_line_2}'

    
