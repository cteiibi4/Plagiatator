from django.urls import path
from .views import PlagitatorView

app_name = "plagiatator"

urlpatterns = [
    path('/', PlagitatorView.as_view()),
]