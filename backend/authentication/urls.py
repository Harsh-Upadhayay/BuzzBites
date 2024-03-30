from django.http import JsonResponse

def sample_response(request):
    data = {
        'message': 'This is a sample response for the API.',
        'status': 'success',
        'data': [
            {'id': 1, 'name': 'Meme 1'},
            {'id': 2, 'name': 'Meme 2'},
            # Add more sample data as needed
        ]
    }
    return JsonResponse(data)

from django.urls import path

urlpatterns = [
    path('', sample_response)    
]

