from django.urls import path
from core import views

urlpatterns = [
    path("", views.calendar_view, name="home"),
    path("test/", views.test, name="test"),
]
