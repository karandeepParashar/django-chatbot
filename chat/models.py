from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields import AutoField, CharField

# Create your models here.
# Image Class
class Image(models.Model):
      imageId = models.AutoField(primary_key= True)
      imagePath = models.CharField(max_length=1200)

# Game class
class Game(models.Model):
      gameId = models.AutoField(primary_key = True)
      user = models.ForeignKey(User, on_delete = models.CASCADE)

# Round class
class Round(models.Model):
      game = models.ForeignKey(Game, on_delete=models.CASCADE)
      round = models.IntegerField(unique = False)
      userImages = models.ManyToManyField(Image, related_name= 'userImages')
      botImages = models.ManyToManyField(Image, related_name= 'botImages')
      commonImages = models.ManyToManyField(Image, related_name= 'commonImages')
      userSelectedImages = models.ManyToManyField(Image, related_name= 'userSelectedImages')
      botSelectedImages = models.ManyToManyField(Image, related_name= 'botSelectedImages')
      
# Message class
class Message(models.Model):
     sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name='sender')        
     receiver = models.ForeignKey(User, on_delete= models.CASCADE, related_name='receiver')
     roundId = models.ForeignKey(Round, on_delete = models.CASCADE)
     message = models.CharField(max_length=1200)
     timestamp = models.DateTimeField(auto_now_add=True)
     def __str__(self):
           return self.message
     class Meta:
           ordering = ('timestamp',)