from django.db import models
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.

class Cast(models.Model):
    name = models.CharField(max_length=80)
    image_url = models.URLField(max_length=1000,null=True)
    in_option = models.BooleanField(default=False)

class Movie(models.Model):
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=300)
    year = models.IntegerField()
    rating = models.FloatField(validators=[MinValueValidator(1.0),MaxValueValidator(10.0)])
    casts = models.ManyToManyField(Cast,related_name="movies",default=list)
    genres = models.CharField(max_length=300,default="")
    poster = models.CharField(max_length=1000,default="")
    plot = models.CharField(max_length=3000,default="")
    popularity = models.FloatField(null=True)
    vote_count = models.IntegerField(null=True)
    in_slider = models.BooleanField(default=False)
    backdrop_url = models.CharField(max_length=1000,null=True)
    awards = models.TextField(null=True,blank=True)
    imdb_rating = models.FloatField(null=True,blank=True)
    imdb_votes = models.IntegerField(null=True,blank=True)
    rotten_tomatoes = models.CharField(max_length=10,null=True,blank=True)
    budget = models.BigIntegerField(null=True,blank=True)
    revenue = models.BigIntegerField(null=True,blank=True)
    runtime = models.IntegerField(null=True,blank=True)


class Comment(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50,blank=True)
    comment = models.CharField(max_length=1500)
    created_at = models.DateTimeField(auto_now_add=True)
    movies = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='comments')
    avatar = models.CharField(max_length=2,null=True)