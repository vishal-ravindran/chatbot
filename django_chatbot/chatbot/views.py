from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import redirect, render
import os
from dotenv import load_dotenv
import openai
from django.contrib import auth
from django.contrib.auth.models import User

from .models import Chat

load_dotenv()

# Create your views here.
OPENAI_API_KEY = os.environ.get('OPEN_AI_SECRET_KEY')
openai.api_key = OPENAI_API_KEY


def ask_chatgpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # print(response)
    result = response['choices'][0]['message']['content'].strip()
    return result


def chatbot(request):
    chats = Chat.objects.filter(user=request.user).order_by('created_at')

    if request.method == 'POST':
        message = request.POST.get('message', '')
        response = ask_chatgpt(message)

        chat = Chat(user=request.user, message=message,
                    response=response, created_at=timezone.now())
        chat.save()

        return JsonResponse({'response': response})
    return render(request, 'chatbot.html', {'chats': chats})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            error_message = 'user not found'
            return render(request, 'login.html', {'error_message': error_message})

    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error creating account'
                return render(request, 'register.html', {'error_message': error_message})
        else:
            error_message = "Passwords don't match"
            return render(request, 'register.html', {'error_message': error_message})

    return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return redirect('/login')
