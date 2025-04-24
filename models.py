from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, user_type=None):
        if not username:
            raise ValueError("User must have username")
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, user_type=user_type)
        user.set_password(password)
        user.save(using=self.db)
        return user
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            user_type='admin'
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
# Base User Model
class CustomUser(AbstractBaseUser):
    USER_TYPES = (('donor', 'Donor'), ('ngo', 'NGO'))

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    is_donor = models.BooleanField(default=False)
    is_ngo = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'user_type']
    
    def __str__(self):
        return self.username

class Donor_Registers(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    dob = models.DateField()
    contact = models.CharField(max_length=15)
    address = models.TextField()
    email = models.EmailField(unique=True)
    designation = models.CharField(max_length=255)
    pan = models.CharField(max_length=10)

    def __str__(self):
        return self.username

class Ngo_Registers(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200)  # Store password securely
    registration_date = models.DateField()
    certified_status = models.CharField(max_length=50, choices=[('registered', 'Registered'), ('not-registered', 'Not Registered')])
    certificates = models.FileField(upload_to='certificates/', null=True, blank=True)
    causes = models.TextField()  # You can store a comma-separated list or serialize the data
    address = models.TextField()
    contact = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    description = models.TextField()
    bank_details = models.TextField()

    def __str__(self):
        return self.name