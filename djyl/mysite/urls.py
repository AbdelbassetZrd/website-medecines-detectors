from django.urls import path
from . import views

urlpatterns = [
    path('video_feed/', views.video_feed, name='video_feed'),
    path('live/', views.video_page, name='video_page'),
    path('detection-info/', views.detection_info, name='detection_info'),
]
