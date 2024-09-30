from django.utils.deprecation import MiddlewareMixin

from company.models import Company

class SubdomainMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Extracción del subdominio de la solicitud

        host = request.get_host()

        # Si es localhost, entonces manejar el subdominio correctamente
        if len(host) > 2 and host[-14:-5] == 'localhost':
            request.subdomain  = host.split('.')[0]
        else:
            request.subdomain = None
        
        if request.subdomain:
            try:
                request.company = Company.objects.get(subdomain=request.subdomain )
            except Company.DoesNotExist:
                request.company = None