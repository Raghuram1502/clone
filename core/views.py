from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
from django.urls import reverse
from .models import Post,Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,authenticate

# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('created_at')
    return render(request,"core/index.html",{"posts":posts})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
        return render(request,"core/register.html",{"form":form})
    else:
        form = UserCreationForm()
        return render(request,"core/register.html",{"form":form})
    
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"core/login.html",{
                "message" : "Invalid ID"
            })
    return render(request,"core/login.html")

@login_required
def logout_view(request):
    logout(request)
    return render(request,"core/login.html")

@login_required
def create_post(request):
    if request.method == "POST":
        image = request.FILES['image']
        caption = request.POST['caption']
        post = Post.objects.create(user=request.user, image=image, caption=caption)
        return redirect('index')
    return render(request, 'instagram/create_post.html')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        body = request.POST['body']
        Comment.objects.create(post=post, user=request.user, body=body)
    return redirect('index')

