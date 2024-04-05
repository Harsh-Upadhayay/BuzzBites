# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('daemonstatus/', views.DaemonStatusAPIView.as_view(), name='daemon_status'),
    # path('addversion/', views.AddVersionAPIView.as_view(), name='add_version'),
    path('schedulespider/', views.ScheduleSpiderAPIView.as_view(), name='schedule_spider'),
    path('cancelspider/', views.CancelSpiderAPIView.as_view(), name='cancel_spider'),
    path('listprojects/', views.ListProjectsAPIView.as_view(), name='list_projects'),
    path('listversions/', views.ListVersionsAPIView.as_view(), name='list_versions'),
    path('listspiders/', views.ListSpidersAPIView.as_view(), name='list_spiders'),
    path('listjobs/', views.ListJobsAPIView.as_view(), name='list_jobs'),
    # path('deleteversion/', views.DeleteVersionAPIView.as_view(), name='delete_version'),
    # path('deleteproject/', views.DeleteProjectAPIView.as_view(), name='delete_project'),
]
