from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from news.views import NewsView

urlpatterns = [
    path('news/', NewsView.as_view({'get': 'get', 'post': 'post'}), name='news'),
    path('news/<int:pk>/', NewsView.as_view({'get': 'get_by_id', 'delete': 'delete'}), name='news'),
    path('special/', NewsView.as_view({'get': 'get_by_type'}), name='special'),
]
