from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.mitra)
admin.site.register(models.grade)
admin.site.register(models.komoditas)
admin.site.register(models.produk)
admin.site.register(models.panenmitra)
admin.site.register(models.detailpanenmitra)
admin.site.register(models.panenlokal)
admin.site.register(models.detailpanenlokal)
admin.site.register(models.pasar)
admin.site.register(models.penjualan)
admin.site.register(models.detailpenjualan)
admin.site.register(models.produksi)
admin.site.register(models.detailproduksi)
admin.site.register(models.jenisbiaya)
admin.site.register(models.biaya)