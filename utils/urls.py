from django.urls import path
from .views import  import_buyers_csv, ticket_create, ticket_detail, ticket_list

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('import-buyers-csv/', import_buyers_csv, name='import_buyers_csv'),

    path('tickets/', ticket_list, name='ticket_list'),
    path('tickets/create/', ticket_create, name='ticket_create'),
    path('tickets/<int:ticket_id>/', ticket_detail, name='ticket_detail'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
