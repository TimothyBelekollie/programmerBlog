from django.contrib import admin
from .models import  Category, BlogPost, Comment, Like, User
# Register your models here.
admin.site.register(User)
admin.site.register(Category)   
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Like)