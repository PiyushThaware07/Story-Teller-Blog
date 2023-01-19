from django.shortcuts import render,redirect,HttpResponseRedirect
# Model
from .models import *

# Date
import datetime

# random
import random

# Pagination
from django.core.paginator import Paginator

# Auth : SignUp
from django.contrib.auth import authenticate,login,logout

# File System Storage
from django.core.files.storage import FileSystemStorage
from .models import *

# templatestag
from .templatetags import extras


# Create your views here.
def home(request):
    allPosts = Post.objects.all()
    recentPosts = Post.objects.all().order_by('-date_timeStamp')
    allCategory = Category.objects.all()
    return render(request, 'Home.html',locals())

def about(request):
    allCategory = Category.objects.all()
    return render(request, 'About.html',locals())

def contact(request):
    allCategory = Category.objects.all()
    if request.method == "POST":
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Message = request.POST.get('message')
        try:
            data_save = Contact(name=Name,email=Email,message=Message)
            data_save.save()
            contact_message = "yes"
        except Exception as e:
            print("Error")   
            contact_message = "no"
            return render(request, 'Home.html',locals())
    return render(request, 'Home.html',locals())

def post(request,pid):
    allPosts = Post.objects.all()
    allCategory = Category.objects.all()
    post = Post.objects.filter(post_id=pid).first()
    more_post = Post.objects.all().exclude(post_id=pid)
    generate_more_post = [random.choice(more_post) for i in allPosts]
    # comment
    comments = CommentModel.objects.filter(get_post=post,reply_on_comment=None)
    # section
    replies = CommentModel.objects.filter(get_post=post).exclude(reply_on_comment=None) # getting only reply
    replyDict = {}
    for reply in replies:
        if reply.reply_on_comment.comment_id not in replyDict.keys():
            replyDict[reply.reply_on_comment.comment_id] = [reply]
        else:
            replyDict[reply.reply_on_comment.comment_id].append(reply)  
    
    return render(request, 'Post.html',locals())

def blog(request):
    allPosts = Post.objects.all().order_by('-date_timeStamp')

    allCategory = Category.objects.all()

    # PAGINATION
    paginator = Paginator(allPosts, 6)           # Item Per Page
    page_number = request.GET.get('page')        # Getting Page No
    allPosts = paginator.get_page(page_number)   # Connection Page No with Page
    last = allPosts.paginator.num_pages          # total no of pages
    totalPageList = [n+1 for n in range(last)]   # 1,2,3

    return render(request, 'Blog.html',locals())

def category(request,cid):
    allCategory = Category.objects.all()
    get_category = Category.objects.get(Category_id=cid)
    allPosts = Post.objects.all().filter(category=get_category)

    # PAGINATION
    paginator = Paginator(allPosts, 6)           # Item Per Page
    page_number = request.GET.get('page')        # Getting Page No
    allPosts = paginator.get_page(page_number)   # Connection Page No with Page
    last = allPosts.paginator.num_pages          # total no of pages
    totalPageList = [n+1 for n in range(last)]   # 1,2,3

    
    return render(request, 'Category.html',locals())


def signup(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pwd = request.POST.get('password1')
        try:
            new_user = User.objects.create_user(first_name=fname,last_name=lname,username=email,password=pwd) 
            new_user.save()
            create_account="yes"
        except:
            create_account="no"
    return render(request, 'Home.html',locals())


def signin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password1']
        user = authenticate(username=email,password=password)
        if user:
            login(request,user)
            login_message = 'yes'
        else:
            login_message = 'no'    
    return render(request, 'Home.html',locals())

def signout(request):
    if not request.user.is_authenticated:
        return redirect('home')
    logout(request)
    logout_message = "yes"
    return render(request, 'Home.html',locals())


def upload(request):
    if not request.user.is_authenticated:
        return redirect('home')
    allPosts = Post.objects.all()
    allCategory = Category.objects.all()
    if request.method == "POST" and request.FILES['myfile']:
        image = request.FILES['myfile']
        title = request.POST.get('title')
        content = request.POST.get('content')
        addcategory = request.POST.get('AddCategory')
        get_category = request.POST.get('category')
        if get_category == "None":
            category = Category(name=addcategory)
            category.save()
        else:    
            category = Category.objects.get(name=get_category)
        date = request.POST.get('date')
        user = request.user
        # file system storage
        fs = FileSystemStorage()
        filename = fs.save(image.name,image)
        url = fs.url(filename)
        
        new_post = Post(thumbnail=url,title=title,content=content,category=category,date_timeStamp=date,user=user)
        try:
            new_post.save()
            return redirect("blog")
            upload_message = "yes"
        except Exception as e:
            print(e)    
            return redirect("home")
            upload_message = "no"
        
    return render(request, 'Upload.html',locals())


def search(request):
    allPosts = Post.objects.all()
    allCategory = Category.objects.all()
    # PAGINATION
    paginator = Paginator(allPosts, 6)           # Item Per Page
    page_number = request.GET.get('page')        # Getting Page No
    allPosts = paginator.get_page(page_number)   # Connection Page No with Page
    last = allPosts.paginator.num_pages          # total no of pages
    totalPageList = [n+1 for n in range(last)]   # 1,2,3

    if request.method == "GET":
        search_item = request.GET.get('search')
        if search_item:
            post_title = Post.objects.filter(title__icontains=search_item)
            post_content = Post.objects.filter(content__icontains=search_item)
            post_writer = Post.objects.filter(user__first_name__contains=search_item)
            post_category = Post.objects.filter(category__name__contains=search_item)
            allPosts = post_title.union(post_content,post_category,post_writer)
            return render(request, 'Search.html',locals())


    return render(request, 'Search.html',locals())


def comment(request):
    if request.method == "POST":
        user = request.user
        postID = request.POST.get('postID')
        post = Post.objects.get(post_id=postID)
        commentMSG = request.POST.get('commentMSG')

        parentID = request.POST.get('parentSno')

        if parentID == "":
            comment = CommentModel(user=user,comment_message=commentMSG,get_post=post)
            comment.save()
        else:
            reply = CommentModel.objects.get(comment_id=parentID)
            comment = CommentModel(user=user,comment_message=commentMSG,get_post=post,reply_on_comment=reply)
            comment.save()
        return redirect(f"/post/{post.post_id}")