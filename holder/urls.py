from django.contrib import admin
from django.urls import path

from .views import IndexPage, ResultPage

urlpatterns = [
    path('', IndexPage.as_view()),
    path('result/<str:result_id>', ResultPage.as_view(), name='result'),
]
