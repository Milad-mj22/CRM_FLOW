from django.urls import path

from .views import  create_coope , coops_by_state , coop_detail,coop_dashboard,coop_state_detail, create_english_invoice, create_preinvoice_view, cutting_factory_create_view, cutting_factory_delete_view, cutting_factory_edit_view, cutting_factory_view, delete_driver_view, delete_group, delete_step, driver_list_view, dynamic_step_view, edit_driver, export_group_excel, manage_access, manage_attribute_groups, manage_coop_attributes, manage_step, register_driver, show_preinvoce_result, steps_list
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [


    path('create_coope/', create_coope, name='show_flow'),

    path('coops/', coops_by_state, name='coop_list'),
    path('coops/<int:coop_id>/', coop_detail, name='coop_detail'),
    path('dashboard/', coop_dashboard, name='coop_dashboard'),

    path('register/driver/', register_driver, name='register_driver'),
    path('drivers/', driver_list_view, name='driver_list'),
    
    path('drivers/edit/<int:driver_id>/', edit_driver, name='edit_driver'),
    path('drivers/delete/<int:driver_id>/', delete_driver_view, name='delete_driver'),
    
    path('admin/coop-attributes/', manage_coop_attributes, name='manage_coop_attributes'),
    path('admin/manage_access/', manage_access, name='manage_access'),

    path('<str:url_name>/<int:order_id>/', dynamic_step_view, name='dynamic_step'),


    # urls.py
    path('admin/attribute-groups/', manage_attribute_groups, name='attribute_group_view'),
    path('group/<int:pk>/delete/', delete_group, name='delete_group'),

    path('export-group/<int:group_id>/', export_group_excel, name='export_group_excel'),




    path('admin/steps/', steps_list, name='steps_list'),
    path('admin/steps/create/', manage_step, name='create_step'),
    path('admin/steps/edit/<int:step_id>/', manage_step, name='edit_step'),
    path('admin/steps/delete/<int:step_id>/', delete_step, name='delete_step'),

    path('preInvoice/', create_preinvoice_view, name='driver_list'),
    path('preinvoice/preview/<str:filename>/', show_preinvoce_result, name='preview_preinvoice'),
    path('create-english-invoice/', create_english_invoice, name='create_english_invoice'),
    



    path('admin/cutting_factory/', cutting_factory_view, name='cutting_factory_list'),
    path('admin/cutting_factory/create/', cutting_factory_create_view, name='cutting_factory_create'),
    path('admin/cutting_factory/edit/<int:pk>/', cutting_factory_edit_view, name='cutting_factory_edit'),
    path('admin/cutting_factory/delete/<int:pk>/', cutting_factory_delete_view, name='cutting_factory_delete'),











]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
