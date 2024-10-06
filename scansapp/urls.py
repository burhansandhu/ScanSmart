from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_image, name='upload_image'),
    path('create_qr/', views.create_qr_code, name='create_qr'),
    path('generate_qr/', views.generate_qr_code, name='generate_qr'),
]
