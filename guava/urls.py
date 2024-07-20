from django.urls import path
from . import views

urlpatterns = [
    # CRUD MITRA
    path('read_mitra/', views.read_mitra,name='read_mitra'),
    path('create_mitra', views.create_mitra,name='create_mitra'),
    path('update_mitra/<str:id>', views.update_mitra,name='update_mitra'),
    path('delete_mitra/<str:id>', views.delete_mitra,name='delete_mitra'),
]