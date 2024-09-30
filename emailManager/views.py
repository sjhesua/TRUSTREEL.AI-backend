from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

def crear_conversacion(request):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "7c54a1944ac84ac2ab26d741777f7b9e"
    }

    data = {
        "replica_id": "r0104286ea",
        "persona_id": "p615a0e4"
    }

    response = requests.post(
    'https://tavusapi.com/v2/conversations', 
    headers=headers, 
    json=data
    )

    return response.json()

def end_conversation(request, conversation_id):
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "7c54a1944ac84ac2ab26d741777f7b9e"
    }

    response = requests.post(
        f'https://tavusapi.com/v2/conversations/{conversation_id}/end', 
        headers=headers
    )

    try:
        response_data = response.json()
    except json.JSONDecodeError:
        response_data = {'error': 'Invalid JSON response'}

    return response_data

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        subject = data.get('subject')
        message = data.get('message')
        recipient = data.get('recipient')
        
        html_message = f"""
        <html>
            <body>
                <p>Visita la conversación <a href="http://localhost:3000/conferencia">aquí</a>.</p>
            </body>
        </html>
        """

        send_mail(
            subject,
            message,
            'jhesua0208@hotmail.com',
            [recipient],
            fail_silently=False,
            html_message=html_message
        )
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def ejecutar_crear_conversacion(request):
    if request.method == 'GET':
        conversation_data = crear_conversacion(request)
        return JsonResponse(conversation_data, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def ejecutar_end_conversation(request, conversation_id):
    if request.method == 'POST':
        conversation_data = end_conversation(request, conversation_id)
        return JsonResponse(conversation_data, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)