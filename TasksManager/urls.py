from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from TasksManager import views



urlpatterns = [
    path('dashboard/calendar/', views.calendar_view, name='calendar_dashboard'),
    path('user-tasks/', views.user_tasks_json, name='user_tasks_json'),
    path('update-task/<int:task_id>/', views.update_task, name='update_task'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
