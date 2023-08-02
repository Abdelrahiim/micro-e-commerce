from Micro.products.views import main
from django.urls import path

urlpatterns = [
    path('',main,name = "main")
]
