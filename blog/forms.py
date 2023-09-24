from django.forms import ModelForm
#from django.contrib.auth.models import User
from .models import BlogPost, User
from django.contrib.auth.forms import UserCreationForm



class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class BlogForm(ModelForm):
 class Meta:
        model=BlogPost
        fields='__all__'
        exclude=['author','contributors']

 
class UserForm(ModelForm):
 class Meta:
        model=User
        fields=['name','username','email','avatar','bio',]
        
        