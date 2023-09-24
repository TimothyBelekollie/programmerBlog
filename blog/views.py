from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from .models import Category, BlogPost, Comment,User

#from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import BlogForm, UserForm, MyUserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm


def loginPage(request):
    page="login"
    
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        email=request.POST.get('email').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(email=email) #check whether the user exist in the db
        except:
            messages.error(request, "User does not exist.") #flash message in django documentation
        user=authenticate(request, email=email, password=password) # check whether the credentials are correct
        if(user is not None): #  if it is correct pass in the login method to save the session the the db and the browser.
            login(request, user) # save the session in the db and the browser.
            return redirect('home') # redirect to the desire page that you want them to be redirected to most often dashboard.
        else:
            messages.error(request, "Incorrect Credentials.") #flash message in django documentation
            
               
    context={"page":page}
    return render(request, 'blog/login_register.html',context)


def registerPage(request):
  
   form=MyUserCreationForm()
   if request.method=='POST':
        form=MyUserCreationForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'An error occur during registration')
    
   return render(request, 'blog/login_register.html',{'form':form})



def logoutUser(request):
    logout(request)
    return redirect('home')



def userProfile(request, pk):
    user=User.objects.get(id=pk)
    blogs=user.blogpost_set.all()
    comments=user.comment_set.all()
    categoriess=Category.objects.all()
    context={'user':user,'blogs':blogs,'comments':comments,'categoriess':categoriess}
    return render(request,'blog/user_profile.html',context)

@login_required(login_url='login')
@login_required(login_url='login')
def updateUser(request):
    user=request.user
    form=UserForm(instance=user)
    if request.method=='POST':
       
        
        form=UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userprofile',pk=user.id)
            
        
    return render(request,'blog/update-user.html',{'form':form})




def home(request):
    q=request.GET.get('q') if request.GET.get('q') !=None else ''
    blogs=BlogPost.objects.filter(
        Q(category__name__icontains=q) |
        Q(title__icontains=q) |
        Q(content__icontains=q) 
       
        
        ).order_by('-created_at')
    categories=Category.objects.all()[0:5]
    blog_count=blogs.count()
    #commentTotal = blogs.comment_set.all().count()
    comments = Comment.objects.filter(
    Q(post__category__name__icontains=q) |  # Assuming post is the ForeignKey to BlogPost
    Q(post__title__icontains=q) |
    Q(post__content__icontains=q)
)
    
    context={'blogs':blogs,'categories':categories,
             'blog_count':blog_count,'comments':comments}
    return render(request, 'blog/index.html', context)



def blog(request,pk):
    blog=BlogPost.objects.get(id=pk)
    blogComments=blog.comment_set.all().order_by('-created_at') # 1 to many relationship
    contributors=blog.contributors.all() # many to many relation.
    if request.method=='POST':
        comment=Comment.objects.create(
            user=request.user,
            post=blog,
            text=request.POST.get('text')
        )
        #blog.participants.add(request.user) # If if a user is not in the room when he send a message there he should automatically be there.
        return redirect('blog',pk=blog.id)

    context={'blog':blog,'blogComments':blogComments,'contributors':contributors}
    return render(request,'blog/blog.html', context)

@login_required(login_url='login')
#create blog
def createBlog(request):
    form=BlogForm()
    categories=Category.objects.all()
    if request.method =='POST':
            category_name=request.POST.get('category')
            category, created=Category.objects.get_or_create(name=category_name)
            uploaded_image = request.FILES.get('image')
            if uploaded_image:
                
                
                blog_post=BlogPost.objects.create(
                author=request.user,
                category=category,
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                
                image=uploaded_image
                
            )
            else:
            
                blog_post = BlogPost.objects.create(
                author=request.user,
                category=category,
                title=request.POST.get('title'),
                content=request.POST.get('content'),
                
            )
            return redirect('home')

        

    
    context= {"form":form,'categories':categories}
    return render(request,'blog/create_blog.html', context) 



def updateBlog(request, pk):
    blog = get_object_or_404(BlogPost, id=pk)
    categories = Category.objects.all()

    if request.user != blog.author:
        return HttpResponse('You are not allowed to update this blog!!.')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
       
            # Check if a new image is uploaded
        uploaded_image = request.FILES.get('image')
        if uploaded_image:
            # Delete the previous image file (if it exists)
            if blog.image:
                blog.image.delete()
            # Assign the new uploaded image
            blog.image = uploaded_image
        # Update other fields
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)
        blog.title = request.POST.get('title')
        blog.category = category
        blog.content = request.POST.get('content')
        # Save the blog post
        blog.save()
        return redirect('home')
    else:
        form = BlogForm(instance=blog)

    context = {'form': form, 'categories': categories, 'blog': blog}
    return render(request, 'blog/edit_blog.html', context)

@login_required(login_url='login')
def deleteBlog(request,pk):
    blog=BlogPost.objects.get(id=pk)
    if request.user != blog.author:
        return HttpResponse('You are not allowed to delete this blog!!.')
    if request.method=='POST':
        blog.image.delete()
        blog.delete()
        return redirect('home')
    return render(request, 'blog/delete.html',{'obj':blog})

@login_required(login_url='login')
def deleteComment(request,pk):
    comment=Comment.objects.get(id=pk)
    if request.user != comment.user:
        return HttpResponse('You are not allowed to delete this comment!!.')
    if request.method=='POST':
        comment.delete()
        return redirect('home')
    return render(request, 'blog/delete.html',{'obj':comment})
