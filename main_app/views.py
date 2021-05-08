from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def home(request):
    return render(request, 'index.html')



def register(request):
    if request.method == "POST":
        errors = User.objects.user_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            print(hashed_pw)
            
            user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'], 
                email = request.POST['email'], 
                password = hashed_pw
            )
            request.session['user_id'] = user.id

            return redirect('/bright_ideas')
            #main page of the application
        return redirect('/')  


def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if len(user) > 0:
        user = user[0]
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        return redirect('/bright_ideas')
    messages.error(request, "Email or password is incorrect")
    return redirect('/')

def idea(request):
    if 'user_id' not in request.session:
        messages.error(request, "You have to log in!")
        return redirect('/')
    context = {
        'user': User.objects.get(id = request.session['user_id']),
        'wall_messages': Message.objects.all()

    }
    return render(request, 'ideas.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def message_post(request):
    Message.objects.create(message=request.POST['message'], poster=User.objects.get(id=request.session['user_id']))
    return redirect('/bright_ideas')

def comment_post(request, wall_message_id):
    poster = User.objects.get(id =request.session['user_id'])
    message = Message.objects.get(id=wall_message_id)
    Comment.objects.create(comment=request.POST['comment'], poster=poster, wall_message=message)
    return redirect('/bright_ideas')



def user_page(request, user_id):
        user = User.objects.get(id=user_id)
        
        context = {
            'one_user': user
    }
        return render(request, 'show_one.html', context)

def liked_ideas(request, user_id):
    liked_message = Message.objects.get(id=user_id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/bright_ideas')


def delete_message(request, user_id):
    destroyed = Message.objects.get(id=user_id)
    destroyed.delete()
    return redirect('/bright_ideas')

