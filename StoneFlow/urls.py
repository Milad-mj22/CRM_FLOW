from django.urls import path

from .views import create_coope , coops_by_state , coop_detail,coop_dashboard,coop_state_detail, register_driver
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [


    path('create_coope/', create_coope, name='show_flow'),

    path('coops/', coops_by_state, name='coop_list'),
    path('coops/<int:coop_id>/', coop_detail, name='coop_detail'),
    path('dashboard/', coop_dashboard, name='coop_dashboard'),
    path('coop/<int:coop_id>/state/<str:state>/', coop_state_detail, name='coop_state_detail'),

    path('register/driver/', register_driver, name='register_driver'),
    

    # path('orders/show_flow/<int:order_id>', show_flow, name='show_flow'),

    # path('section1/<int:order_id>/', section1_view, name='section1_url'),
    # path('section2/<int:order_id>/', section2_view, name='section2_url'),
    # path('section3/<int:order_id>/', section3_view, name='section3_url'),
    # path('section4/<int:order_id>/', section4_view, name='section4_url'),


    # path('edit-request/<int:order_id>/<int:step_number>/', edit_request, name='edit_request')


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
