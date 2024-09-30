from django.urls import path
from .views import UploadExcelView,UserClientsView,ClientCreateView,ClientDeleteView

urlpatterns = [
    path('upload-excel/', UploadExcelView.as_view(), name='upload-excel'),
    path('search-clients/', UserClientsView.as_view(), name='user-clients'),
    path('delete-clients/<int:id>/', ClientDeleteView.as_view(), name='client-delete'),
    path('add-clients/', ClientCreateView.as_view(), name='client-create'),
]