from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.views import View
from client.models import Client
from client.forms import ClientForm

class CustomLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('../dashboard')  # Redirige al dashboard si el usuario ya está autenticado
        return render(request, 'users/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('../dashboard')  # Redirige al dashboard después del login
        else:
            return render(request, 'users/login.html', {'error': 'Invalid username or password'})

class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('../login')  # Redirige al login después del logout
     
class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html')

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email, password=password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('../dashboard')  # Redirige al dashboard después del registro
        else:
            return render(request, 'users/register.html', {'error': 'Registration failed'})

@login_required(login_url='/users/login/')
def DashboardView(request):
    form = ClientForm()
    if request.method == 'POST':
        if 'client_id' in request.POST:
            # Eliminar cliente
            client_id = request.POST.get('client_id')
            if client_id:
                try:
                    client = Client.objects.get(id=client_id)
                    client.delete()
                except Client.DoesNotExist:
                    pass
        else:
            # Registrar cliente
            form = ClientForm(request.POST)
            if form.is_valid():
                client = form.save(commit=False)
                client.user = request.user
                client.save()
                return redirect('../dashboard')

    clients = Client.objects.filter(user=request.user)
    return render(request, 'users/dashboard.html', {'username': request.user.username, 'clients': clients, 'form': form})
