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
    # CUD DETAIL PENJUALAN
    path('update_detail_penjualan/<str:id>', views.update_detail_penjualan,name='update_detail_penjualan'),
    path('delete_detail_penjualan/<str:id>', views.delete_detail_penjualan,name='delete_detail_penjualan'),
    path('create_detail_penjualan/<str:id>', views.create_detail_penjualan,name='create_detail_penjualan'),
    # CRUD PRODUK
    path('create_produk', views.create_produk,name='create_produk'),
    path('read_produk', views.read_produk,name='read_produk'),
    path('update_produk/<str:id>', views.update_produk,name='update_produk'),
    path('delete_produk/<str:id>', views.delete_produk,name='delete_produk'),
    # CRUD KOMODITAS
    path('create_komoditas', views.create_komoditas,name='create_komoditas'),
    path('read_komoditas', views.read_komoditas,name='read_komoditas'),
    path('update_komoditas/<str:id>', views.update_komoditas,name='update_komoditas'),
    path('delete_komoditas/<str:id>', views.delete_komoditas,name='delete_komoditas'),
    # CRUD PASAR
    path('create_pasar', views.create_pasar,name='create_pasar'),
    path('read_pasar', views.read_pasar,name='read_pasar'),
    path('update_pasar/<str:id>', views.update_pasar,name='update_pasar'),
    path('delete_pasar/<str:id>', views.delete_pasar,name='delete_pasar'),
]