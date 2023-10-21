from django.http import JsonResponse
from django.shortcuts import render
import os
from dotenv import load_dotenv
import openai


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

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_chatgpt(message)

        return JsonResponse({'response': response})
    return render(request, 'chatbot.html')
