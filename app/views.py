from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from .forms import userForm , ProfileForm, UserChange
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Profile, Post, Announcement
from django.core.files.storage import FileSystemStorage 
from .filters import AnnouncementFilter
from django.db.models import F
import requests
import datetime
import re



@login_required(login_url='login_view')
def home(request):
    q = 'COVID-19'
    size = '5'
    today = str(datetime.date.today())
    yesterday = str(datetime.date.today()- datetime.timedelta(days=1))
    if request.method == 'POST':
        q = request.POST['q']
        size = request.POST['size']
    response = requests.get('http://newsapi.org/v2/everything?'
    'q=' + q + '&'
    'domains=record.pt,publico.pt,sicnoticias.pt,sapo.pt,abola.pt,jn.pt,cmjornal.pt,dn.pt,rtp.pt&'
    'from=' + yesterday +'&'
    'to=' + today + '&'
    'pageSize=' + size + '&'
    'sortBy= relevancy&'
    'apiKey=0722d2af4ee4483ea9fcfa950a2d85f6').json()
    context = {'response': response}
    return render(request,'app/home.html', context)


def login_view(request):
    form = userForm()
    if request.method=='POST':
       username = request.POST.get('username')
       password = request.POST.get('password')
       user = authenticate(request, username=username, password = password)
       if user is not None:
           login(request, user)
           messages.success(request,'Autenticado com sucesso')
           return redirect('home') 
       else:
            messages.error(request,'O seu username e a sua password não coincidem')
            return redirect('login_view')
    else:   
        return render(request,'app/login.html',{'form':form})


def register(request):
    form = userForm()
    context = {'form': form}
    if request.method=='POST':
        form = userForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            Profile.objects.create(
				user=user,
                profile_pic = 'profile2.png',
				)
            messages.success(request,'Conta criada com sucesso')    
            return redirect('login_view')  
        else:
            form = userForm()
            context = {'form': form}
            return render(request,'app/register.html', context)   
    else:   
        return render(request,'app/register.html', context)

@login_required(login_url='login_view')
def logoutUser(request):
    logout(request)
    return redirect('login_view')        


@login_required(login_url='login_view')
def accountSettings(request):
    if request.method == 'POST':
        form_profile = ProfileForm(request.POST, request.FILES,instance=request.user.profile)
        form_user = UserChange(request.POST, instance = request.user)
        if form_user.is_valid() and form_profile.is_valid():
            user = form_user.save()
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request,'Alterações guardadas.')
    return render(request, 'app/edit_profile.html')
    

@login_required(login_url='login_view')
def posts(request):
    user = request.user
    posts = Post.objects.filter(reply_to__isnull= True).order_by('-date_created')
    context = {'posts': posts}
    if request.method == 'POST':
        content = request.POST['content']
        try:
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            picturename = fs.save(picture.name, picture)
        except:
            picture = None     
        try:
            yt_link = re.search("((?<=(v|V)/)|(?<=be/)|(?<=(\?|\&)v=)|(?<=embed/))([\w-]+)", content).group()
        except:
            yt_link = None      
        p =Post.objects.create(
            author = user,
            content = content,
            picture = picture,
            yt_link = yt_link,
            )
        messages.success(request, 'Post criado com sucesso')  
        return redirect('post',p.id)    
    return render(request,'app/posts.html',context)  


@login_required(login_url='login_view')
def post(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    comments = Post.objects.filter(reply_to= post).order_by('-date_created') 
    if request.method == 'POST':
        content = request.POST['content']
        try:
            picture = request.FILES['picture']
            fs = FileSystemStorage()
            picturename = fs.save(picture.name, picture)
        except:
            picture = None     
        p = Post.objects.create(
            reply_to = post,
            author = user,
            content = content,
            picture = picture
            )
        post.ncomments += 1
        post.save() 
        context = {'post': post, 'comments': comments} 
        messages.success(request, 'Comentário criado com sucesso')  
        return redirect('post',p.id)   
    if not comments:   
         context = {'post': post}
    else:
         context = {'post': post, 'comments':comments}      
    return render(request, 'app/post.html', context)      


@login_required(login_url = 'login_view')
def upvote(request, pk):
    post = get_object_or_404(Post,pk = pk)
    post.upvotes += 1
    post.save()
    messages.success(request, 'Um gosto foi deixado no post')    
    return redirect('post', post.id)
    


@login_required(login_url = 'login_view')
def downvote(request, pk):
    post = get_object_or_404(Post,pk = pk)
    post.downvotes += 1
    post.save()
    messages.success(request, 'O post foi reportado')
    return redirect('post', post.id)


@login_required(login_url='login_view')
def createa(request):
    user = request.user
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        contact = request.POST['contact']
        category = request.POST['category']
        try:
            picture = request.FILES['imagem']
            print(picture)
            fs = FileSystemStorage()
            picturename = fs.save(picture.name, picture) 
        except:
            picture = 'default-image.jpg'  
        if contact == '':
            contact = user.email
        a = Announcement.objects.create(
            author = user,
            title = title,
            content = content,
            contact = contact,
            category = category,
            picture = picture,
        )
        messages.success(request, 'Anúncio criado com sucesso')
        return redirect('announcement', a.id)
    return render(request, 'app/createa.html')


@login_required(login_url='login_view')
def announcements(request):
    user = request.user
    announcements = Announcement.objects.all().order_by('-date_created') 
    filter = AnnouncementFilter(request.GET, queryset = announcements)
    announcements=filter.qs
    context = {'announcements': announcements,
    'filter':filter}
    return render(request,'app/announcements.html',context)  


@login_required(login_url='login_view')
def announcement(request, pk):
    announcement = Announcement.objects.get(id=pk)
    context = {'announcement': announcement}
    return render(request, 'app/announcement.html', context)

@login_required(login_url = 'login_view')
def report(request, pk):
    announcement = get_object_or_404(Announcement,pk = pk)
    announcement.reports += 1
    announcement.save()
    messages.success(request,'O post foi reportado e será analisado por um adminstrador')
    return redirect('announcement',announcement.id)    


@login_required(login_url='login_view')
@user_passes_test(lambda u: u.is_superuser)
def adminpanel(request):
    posts = Post.objects.filter(downvotes__gt =F('upvotes')).exclude(reviewed = True)
    announcements = Announcement.objects.filter(reports__gt = 0).exclude(reviewed = True)
    context = {'posts': posts,'announcements': announcements}
    return render(request, 'app/adminpanel.html', context) 


@login_required(login_url='login_view')
@user_passes_test(lambda u: u.is_superuser)
def deletepost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        if post.reply_to is not None:
            post.reply_to.ncomments -= 1
            post.reply_to.save()
        post.delete()
        messages.success(request, 'O post foi apagado')
        return redirect('adminpanel')
    context = {'post':post, 'item':'post'}
    return render(request, 'app/delete.html', context)

@login_required(login_url='login_view')
def deleteownpost(request, pk):
    post = Post.objects.get(id=pk)
    if request.method=="POST":   
        if request.user == post.author:
            if post.reply_to is not None:
                post.reply_to.ncomments -= 1
                post.reply_to.save()
            post.delete()
            messages.success(request, 'O post foi apagado')
            return redirect('posts')
        else:
            return HttpResponseForbidden()
    context = {'post':post, 'item':'post'}
    return render(request, 'app/delete.html', context)         


@login_required(login_url='login_view')
@user_passes_test(lambda u: u.is_superuser)
def reviewpost(request, pk):
    post = Post.objects.get(id=pk)
    post.reviewed = True
    post.save()
    return redirect('adminpanel')  



@login_required(login_url='login_view')
@user_passes_test(lambda u: u.is_superuser)
def deletea(request, pk):
    announcement = Announcement.objects.get(id=pk)
    if request.method == "POST":
        announcement.delete()
        messages.success(request, 'O anúncio foi apagado')
        return redirect('adminpanel')
    context = {'announcement':announcement,  'item':'anúncio'}
    return render(request, 'app/delete.html', context) 

@login_required(login_url='login_view')
def deleteowna(request, pk):
    announcement = Announcement.objects.get(id=pk)
    if request.method=="POST":  
        if request.user == announcement.author: 
            announcement.delete()
            messages.success(request, 'O anúncio foi apagado')
            return redirect('announcements')
        else:
            return HttpResponseForbidden()
    context = {'announcement':announcement, 'item':'anúncio'}
    return render(request, 'app/delete.html', context)         


@login_required(login_url='login_view')
@user_passes_test(lambda u: u.is_superuser)
def reviewa(request, pk):
    announcement = Announcement.objects.get(id=pk)
    announcement.reviewed = True
    announcement.save()
    return redirect('adminpanel')    


@login_required(login_url='login_view')
@user_passes_test(lambda u: u.is_superuser)
def deleteuser(request,pk):
    user = User.objects.get(id = pk)
    profile = Profile.objects.get(user = user)
    if request.method == "POST":
        if request.user == user:
            messages.error(request, 'Não se pode apagar a si mesmo')
            return redirect('adminpanel')
        else:    
            user.delete()
            profile.delete()
            messages.success(request, 'O utilizador foi apagado')
            return redirect('adminpanel')
    context = {'user': user, 'item':'utilizador'}
    return render(request, 'app/delete.html', context)

    
@login_required(login_url='login_view')
@user_passes_test(lambda u: u.is_superuser)
def users(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'app/users.html', context)        





                


















