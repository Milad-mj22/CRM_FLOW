from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from dashboard.views import mian_dashboard



urlpatterns = [


    path('', mian_dashboard, name='mian_dashboard'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
