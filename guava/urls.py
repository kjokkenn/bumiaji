from django.urls import path
from . import views

urlpatterns = [
    # CRUD MITRA
    path('create_mitra', views.create_mitra,name='create_mitra'),
    path('read_mitra/', views.read_mitra,name='read_mitra'),
    path('update_mitra/<str:id>', views.update_mitra,name='update_mitra'),
    path('delete_mitra/<str:id>', views.delete_mitra,name='delete_mitra'),
    # CRUD PENJUALAN
    path('create_penjualan', views.create_penjualan,name='create_penjualan'),
    path('read_penjualan', views.read_penjualan,name='read_penjualan'),
    path('update_penjualan/<str:id>', views.update_penjualan,name='update_penjualan'),
    path('delete_penjualan/<str:id>', views.delete_penjualan,name='delete_penjualan'),
]