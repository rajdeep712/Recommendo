from django.db import models
from django.contrib.auth.models import User

from home.models import Movie,Cast


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , related_name="profile")
    is_verified = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=100)
    favourites = models.ManyToManyField(Movie,related_name="profiles",default=list)
    pass_reset_token = models.CharField(max_length=100,blank=True)
    avatar_url = models.CharField(max_length=2000,blank=True)
    firstTime_login_done = models.BooleanField(default=False)
    fav_casts = models.ManyToManyField(Cast,related_name="profiles")