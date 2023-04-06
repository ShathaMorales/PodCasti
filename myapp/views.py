from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from myapp.models import Podcast, Genre, User
from myapp.forms import *
import bcrypt



def index(request):    
    if 'user_id' in request.session:
        user = True
        context = {'user': user}
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


def signup(request):
    return render(request, 'signup.html')


def signupaction(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/signup')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=request.POST['first_name'],
                            last_name=request.POST['last_name'],
                            email=request.POST['email'],
                            user_name=request.POST['user_name'],
                            dob=request.POST['dob'],
                            password=pw_hash)
        return render(request, 'login.html')


def login(request):
    return render(request, 'login.html')


def loginaction(request):
    print('function run')
    user = User.objects.filter(email=request.POST['email']).first()
    if user:
        print('user found')
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            return redirect('/')
        else:
            print('wrong password')
            messages.error(request, "Wrong Password")
            return redirect('/login')
    else:
        print('email not found')
        messages.error(request, "Email not found in the database")
        return redirect('/login')


def addpodcast(request):
    if 'user_id' in request.session:
        if request.method == 'POST':
            loged_user = User.objects.get(id=request.session['user_id'])
            print(loged_user.first_name)
            mp3_form = MP3UploadForm(request.POST, request.FILES)
            if mp3_form.is_valid():
                podcast = mp3_form.save(commit=False)
                podcast.description = request.POST['description']
                podcast.added_by = loged_user
                podcast.save()
                return redirect('/')
        else:
            mp3_form = MP3UploadForm()
        context = {
                'mp3_form': mp3_form
                }
        return render(request, 'add_podcast.html', context)
    else:
        return redirect('/login')


def player(request, podcast_id):
    if 'user_id' in request.session:
        podcast = Podcast.objects.get(id=podcast_id)
        print(Podcast.objects.get(id=podcast_id).file.url)
        print(podcast.added_by)
        return render(request, 'player.html', {'podcast': podcast})
    else:
        return redirect('/login')


def about(request):
    return render(request, 'about.html')


def profile(request):
    if 'user_id' in request.session:
        loged_user = User.objects.get(id=request.session['user_id'])
        podcasts = loged_user.podcasts.all()
        context ={
            'podcasts':podcasts,
            'loged_user':loged_user
        }
        return render(request, 'profile.html', context)
    else:
        return redirect('/')
        
def otherprofile(request, user_id):
    if 'user_id' in request.session:
        user = User.objects.get(id=user_id)
        loged_user = User.objects.get(id=request.session['user_id'])
        podcasts = user.podcasts.all()
        context ={
            'podcasts':podcasts,
            'loged_user':loged_user,
            'user':user,
        }
        return render(request, 'profile.html', context)
    else:
        return redirect('/profile/{user_id}/')      

def library(request):
    if 'user_id' in request.session:
        loged_user = User.objects.get(id=request.session['user_id'])
        podcasts = loged_user.podcasts.all()
        data ={
            'podcasts':podcasts,
            #'loged_user':loged_user,
        }
        return render(request, 'library.html', data)
    else:
        return redirect('/')


def update(request):
    if 'user_id' in request.session:
        loged_user = User.objects.get(id=request.session['user_id'])
        #inf = loged_user.
        context={
            'loged_user':loged_user,
        }    
        return render(request, 'update.html', context)
    else:
        return redirect('/profile')

def signout(request):
    logout(request)
    return redirect('/login')