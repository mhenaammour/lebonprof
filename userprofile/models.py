from django.db import models
from django.contrib.auth.models import User

class Userprofile(models.Model):

    user=models.OneToOneField(User, related_name='userprofile', on_delete=models.CASCADE)
    last_name = models.CharField(max_length=30, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    profile_picture = models.ImageField(upload_to='uploads/annoces_images/', default='https://via.placeholder.com/240x240x.jpg' ,blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username
