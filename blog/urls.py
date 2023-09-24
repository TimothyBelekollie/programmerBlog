from django.urls import path
from . import views


urlpatterns = [
     path('',views.home, name="home"),
     path('login/', views.loginPage, name="login"),
     path('register/', views.registerPage, name="register"),
     path('logout/', views.logoutUser, name="logout"),
     path('update-user/',views.updateUser, name="update-user"),
     path('profile/<str:pk>/',views.userProfile, name="userprofile"),
     path('blog/<str:pk>/',views.blog, name="blog"),
    
     path('create-blog/',views.createBlog, name="create-blog"),
     path('update-blog/<str:pk>/',views.updateBlog, name="update-blog"),
     path('delete-blog/<str:pk>/',views.deleteBlog, name="delete-blog"),
     path('delete-comment/<str:pk>/',views.deleteComment, name="delete-comment"),
     #path('update-user/',views.updateUser, name="update-user"),
    #  path('topics/', views.topicsPage, name="topics"),
    # path('activity/', views.activityPage, name="activity"),
    
]
