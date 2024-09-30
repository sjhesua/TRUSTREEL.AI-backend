from django.shortcuts import render, get_object_or_404
from .models import Company,CustomUser

from .serializers import RegisterSerializer,UserSerializer,MyTokenObtainPairSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        # Imprimir los datos recibidos en la consola
        print("Datos recibidos en la vista:", request.data)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("Errores de validación:", serializer.errors)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    output = f'Este es un mensaje protegido {request.user}'
    return Response({'response': output}, status=status.HTTP_200_OK)

@api_view(['GET'])
def view_all_routes(request):
    routes = [
        {'path': 'api/token/', 'name': 'token-obtain-pair'},
        {'path': 'api/token/verify/', 'name': 'token-verify'},
        {'path': 'api/token/refresh/', 'name': 'refresh-token'},
        {'path': 'api/register/', 'name': 'register-user'},
        {'path': 'api/test/', 'name': 'test'},
        {'path': 'api/help/', 'name': 'all-routes'},
    ]
    return Response(routes)

def subdomain_view(request):
    host = request.get_host()  # Obtener el host de la solicitud
    subdomain = host.split('.')[0]
    print(subdomain)
    #Buesca en la base de datos una compañia con el subdominio que se indica en el url
    #Si no se consigue la compañia se devuelve un error 404
    company = get_object_or_404(Company, subdomain=subdomain)
    #Envia: <p><strong>Nombre:</strong> {{ empresa.name }}</p>
    #       <p><strong>Subdominio:</strong> {{ empresa.subdomain }}</p>
    return render(request, 'company/detalle.html', {'empresa': company})

class CustomTokenVerifyView(TokenVerifyView):
    pass