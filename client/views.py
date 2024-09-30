from .serializers import ClientSerializer
from .models import Client
import pandas as pd
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

class UploadExcelView(APIView):
    def post(self, request, format=None):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            df = pd.read_excel(file)
            added_clients = []
            for _, row in df.iterrows():
                email = row['emails']
                user_id = 1  # Assuming the Excel file has a column 'user_id'
                
                # Check if the email already exists for the user
                if Client.objects.filter(emails=email, user_id=user_id).exists():
                    continue  # Skip this client if the email already exists
                
                client_data = {
                    'emails': email,
                    'names': row['names'],
                    'user': user_id
                }
                serializer = ClientSerializer(data=client_data)
                if serializer.is_valid():
                    client = serializer.save()
                    added_clients.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"success": "File uploaded successfully", "added_clients": added_clients}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserClientsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        clients = Client.objects.filter(user=user)
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)

class ClientCreateView(generics.CreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.id
        print("Datos recibidos en la solicitud:", request.data)
        # Crear el cliente
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            # Imprimir los errores de validación
            print("Errores de validación:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ClientDeleteView(generics.DestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'id'