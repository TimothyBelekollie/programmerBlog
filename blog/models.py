from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.auth.models import User

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
   

# Create your models here.

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     profile_image = models.ImageField(null=True, default="avatar.svg")
#     bio = models.TextField()
    
class Category(models.Model):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class BlogPost(models.Model):
  
    title = models.CharField(max_length=200)
    content = models.TextField()
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    contributors=models.ManyToManyField(User, related_name='contributors', blank=True) # we already have User Model so we don't explicitly use it again we just fine related_name for the User Model
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, default="avatar.svg")
        
    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
         return self.text[0:50]
     
class Like(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
# class Message(models.Model):
#     user=models.ForeignKey(User, on_delete=models.CASCADE)
#     room=models.ForeignKey(BlogPost,on_delete=models.CASCADE)
#     body=models.TextField()
#     updated=models.DateTimeField(auto_now=True)
#     created=models.DateTimeField(auto_now_add=True)
#     class Meta:
#         ordering=['-updated','-created']
    
#     def __str__(self):
#         return self.body[0:50]
