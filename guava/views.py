from django.shortcuts import render, redirect
from . import models
from datetime import datetime
import calendar
# from .decorators import role_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login , logout, authenticate
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.forms import DateInput
from django.db import transaction
from django.core.exceptions import ValidationError
import json
# from weasyprint import HTML
from django.template.loader import render_to_string
import tempfile
from django.urls import reverse
# Create your views here.


# CRUD MITRA
def read_mitra(request) :
    allmitra = models.mitra.objects.all()
    if not allmitra.exists():
        messages.error(request, "Data Mitra Tidak Ditemukan!")
    return render(request,
                  'mitra/read_mitra.html',
                  {
                      'allmitra': allmitra
                  })

def create_mitra(request) :
    
    if request.method == "GET" :
        return render(request, 
                      'mitra/create_mitra.html')
    else :
        namamitra = request.POST["nama_mitra"]
        mitraobj = models.mitra.objects.filter(nama_mitra=namamitra)
        
        if len(mitraobj) >0:
            messages.error(request,"Nama Mitra Sudah Ada")
        else :
            alamatmitra = request.POST["alamat_mitra"]
            nohpmitra = request.POST["nohp_mitra"]
            tanggalawalmitra = request.POST["tanggalawal_mitra"]
            durasikontrakmitra = request.POST["durasi_kontrak"]
            luaslahan = request.POST["luas_lahan"]
            status = request.POST["status_mitra"]
            if status.lower() == "aktif" :
                statusmitra = True
            else :
                statusmitra = False
            models.mitra(
                nama_mitra = namamitra,
                alamat_mitra = alamatmitra,
                nohp_mitra = nohpmitra,
                tanggalawal_mitra = tanggalawalmitra,
                durasi_kontrak = durasikontrakmitra,
                luas_lahan = luaslahan,
                status_mitra = statusmitra
            ).save()

            messages.success(request,"Data Mitra Berhasil Ditambahkan!")
        return redirect("read_mitra")
            

    
def update_mitra(request, id):
    try:
        getmitraobj = models.mitra.objects.get(id_mitra=id)
    except models.mitra.DoesNotExist:
        messages.error(request, "Mitra tidak ditemukan!")
        return redirect('read_mitra')

    if request.method == "GET":
        tanggal = getmitraobj.tanggalawal_mitra.strftime('%Y-%m-%d')  # Format tanggal
        statusmitra = 'Aktif' if getmitraobj.status_mitra else 'Tidak Aktif'
        return render(request, 'mitra/update_mitra.html', {
            'getmitraobj': getmitraobj,
            'statusmitra': statusmitra,
            'tanggal': tanggal
        })
    else:
        namamitra = request.POST.get("nama_mitra")
        
        # Cek apakah nama mitra sudah ada, kecuali untuk objek yang sedang diperbarui
        if models.mitra.objects.filter(nama_mitra=namamitra).exclude(id_mitra=id).exists():
            messages.error(request, "Nama Mitra Sudah Ada!")
            return redirect('read_mitra')

        # Perbarui objek mitra
        getmitraobj.nama_mitra = namamitra
        getmitraobj.alamat_mitra = request.POST.get("alamat_mitra")
        getmitraobj.nohp_mitra = request.POST.get("nohp_mitra")
        getmitraobj.tanggalawal_mitra = request.POST.get("tanggalawal_mitra")
        getmitraobj.durasi_kontrak = request.POST.get("durasi_kontrak")
        getmitraobj.luas_lahan = request.POST.get("luas_lahan")
        getmitraobj.status_mitra = request.POST.get("status_mitra").lower() == "aktif"
        
        getmitraobj.save()
        messages.success(request, "Mitra berhasil diperbarui!")
        return redirect('read_mitra')
            
    
def delete_mitra(request,id) :
    getmitraobj = models.mitra.objects.get(id_mitra = id)
    getmitraobj.delete()
    messages.success(request, "Data berhasil dihapus!")
    return redirect('read_mitra')

'''CRUD PENJUALAN'''
def create_penjualan(request) :
    #Data yang harus diambil sebelum masuk ke 'get'/'post'
    # detailpanenlobj = 
    pasarobj = models.pasar.objects.all()
    produkobj = models.produk.objects.all()
    komoditasobj = models.komoditas.objects.all()
    if request.method == 'GET' :
        return render(request, 'penjualan/create_penjualan.html',{
            'pasarobj' : pasarobj,
            'produkobj' : produkobj,
            'komoditasobj' : komoditasobj,
        })
    
    else :
        #Mengambil data yang ingin di 'post' dari input html
        pasar = request.POST['pasar']
        tanggal = request.POST['tanggal']
        kuantitasp = request.POST.getlist('kuantitasp')
        kuantitask = request.POST.getlist('kuantitask')
        produk = request.POST.getlist('produk')
        komoditas = request.POST.getlist('komoditas')

        print(kuantitasp)
        print(kuantitask)
        print(produk)
        print(komoditas)
        #request.POST.getlist
        #for a,b,c,d in zip(a,b,c,d)


        penjualan = models.penjualan(
            id_pasar = models.pasar.objects.get(id_pasar = pasar),
            tanggal = tanggal,
        )
        penjualan.save()

        id = penjualan.id_penjualan
        iddetail = []

        for produk,komoditas,kuantitasp,kuantitask in zip(produk,komoditas,kuantitasp,kuantitask) :
            if komoditas != '' and produk != '' and kuantitasp != '' and kuantitask != '' :
                detail = models.detailpenjualan(
                    id_penjualan = models.penjualan.objects.get(id_penjualan = id),
                    id_produk = models.produk.objects.get(id_produk = produk),
                    id_komoditas = models.komoditas.objects.get(id_komoditas = komoditas),
                    kuantitas_produk = kuantitasp,
                    kuantitas_komoditas = kuantitask,
                )
                detail.save()
                iddetail.append(detail.iddetail_penjualan)


            elif komoditas != '' and produk == '' and kuantitasp == '' and kuantitask != '' :
                detail = models.detailpenjualan(
                    id_penjualan = models.penjualan.objects.get(id_penjualan = id),
                    id_produk = None,
                    id_komoditas = models.komoditas.objects.get(id_komoditas = komoditas),
                    kuantitas_produk = None,
                    kuantitas_komoditas = kuantitask,
                )
                detail.save()
                iddetail.append(detail.iddetail_penjualan)
            
            elif komoditas == '' and produk != '' and kuantitasp != '' and kuantitask == '' :
                detail = models.detailpenjualan(
                    id_penjualan = models.penjualan.objects.get(id_penjualan = id),
                    id_produk = models.produk.objects.get(id_produk = produk),
                    id_komoditas = None,
                    kuantitas_produk = kuantitasp,
                    kuantitas_komoditas = None,
                )
                detail.save()
                iddetail.append(detail.iddetail_penjualan)

            else :
                getpenjualan = models.penjualan.objects.get(id_penjualan = id)
                getdetailpenjualan = models.detailpenjualan.objects.filter(iddetail_penjualan__in = iddetail)
                getpenjualan.delete()
                getdetailpenjualan.delete()
                messages.error(request, 'Data Penjualan minimal memiliki produk/komoditas dan kuantitas yang sesuai, Coba Ulang Kembali!')
                return redirect('create_penjualan')
        messages.success(request, 'Data Penjualan Berhasil Ditambahkan!')
        return redirect('read_penjualan')
    

def read_penjualan(request) : 
    penjualanobj = models.penjualan.objects.all()
    detailpenjualanobj = models.detailpenjualan.objects.all()
    if not penjualanobj.exists():
        messages.error(request, "Data Penjualan Tidak Ditemukan!")
    return render(request,
                  'penjualan/read_penjualan.html',
                  {
                      'penjualanobj': penjualanobj,
                      'detailpenjualanobj' : detailpenjualanobj,
                  })

    
def update_penjualan(request, id) :
    pasarobj = models.pasar.objects.all()
    produkobj = models.produk.objects.all()
    komoditasobj = models.komoditas.objects.all()

    getpenjualan = models.penjualan.objects.get(id_penjualan = id)
    tanggal_penjualan = datetime.strftime(getpenjualan.tanggal, '%Y-%m-%d')
    id_pasar = getpenjualan.id_pasar.nama_pasar
    print(id_pasar)
    print(getpenjualan.tanggal)
    print(tanggal_penjualan)
    if request.method == 'GET' :
        return render (request, 'penjualan/update_penjualan.html', {
            'tanggalpenjualan' : tanggal_penjualan,
            'id_pasar' : id_pasar,
            'getpenjualan' : getpenjualan,
            'pasarobj' : pasarobj,
            'produkobj' : produkobj,
            'komoditasobj' : komoditasobj,
        })
    
    else :
        pasar = request.POST['pasar']
        tanggal = request.POST['tanggal']
        

        getpenjualan.id_penjualan = getpenjualan.id_penjualan
        getpenjualan.id_pasar = models.pasar.objects.get(id_pasar = pasar)
        getpenjualan.tanggal = tanggal

        getpenjualan.save()
        messages.success(request, "Data Penjualan berhasil diperbarui!")
        return redirect('read_penjualan')

def delete_penjualan(request, id) :
    getpenjualan = models.penjualan.objects.get(id_penjualan = id)
    getpenjualan.delete()
    messages.success(request, "Data Penjualan berhasil dihapus!")
    return redirect('read_penjualan')


'''CUD DETAIL PENJUALAN'''
def create_detail_penjualan(request, id) :
    komoditasobj = models.komoditas.objects.all()
    produkobj = models.produk.objects.all()
    if request.method == 'GET' :
        return render (request, 'penjualan/create_detail_penjualan.html', {
            'komoditasobj' : komoditasobj,
            'produkobj' : produkobj,
        })
    
    else :
        kuantitasp = request.POST.getlist('kuantitasp')
        kuantitask = request.POST.getlist('kuantitask')
        produk = request.POST.getlist('produk')
        komoditas = request.POST.getlist('komoditas')

        iddetail = []

        for produk,komoditas,kuantitasp,kuantitask in zip(produk,komoditas,kuantitasp,kuantitask) :
            if komoditas != '' and produk != '' and kuantitasp != '' and kuantitask != '' :
                detail = models.detailpenjualan(
                    id_penjualan = models.penjualan.objects.get(id_penjualan = id),
                    id_produk = models.produk.objects.get(id_produk = produk),
                    id_komoditas = models.komoditas.objects.get(id_komoditas = komoditas),
                    kuantitas_produk = kuantitasp,
                    kuantitas_komoditas = kuantitask,
                )
                detail.save()
                iddetail.append(detail.iddetail_penjualan)

                print('kondisi 1')


            elif komoditas != '' and produk == '' and kuantitasp == '' and kuantitask != '' :
                detail = models.detailpenjualan(
                    id_penjualan = models.penjualan.objects.get(id_penjualan = id),
                    id_produk = None,
                    id_komoditas = models.komoditas.objects.get(id_komoditas = komoditas),
                    kuantitas_produk = None,
                    kuantitas_komoditas = kuantitask,
                )
                detail.save()
                iddetail.append(detail.iddetail_penjualan)
                print('kondisi 2')
            
            elif komoditas == '' and produk != '' and kuantitasp != '' and kuantitask == '' :
                detail = models.detailpenjualan(
                    id_penjualan = models.penjualan.objects.get(id_penjualan = id),
                    id_produk = models.produk.objects.get(id_produk = produk),
                    id_komoditas = None,
                    kuantitas_produk = kuantitasp,
                    kuantitas_komoditas = None,
                )
                detail.save()
                iddetail.append(detail.iddetail_penjualan)
                print('kondisi 3')

            else :
                getdetailpenjualan = models.detailpenjualan.objects.filter(iddetail_penjualan__in = iddetail)
                getdetailpenjualan.delete()
                print('kondisi 4')
                messages.error(request, 'Data Detail Penjualan minimal memiliki produk/komoditas dan kuantitas yang sesuai, Coba Ulang Kembali!')
                return redirect(reverse('create_detail_penjualan', args =[id]))
            
        messages.success(request, 'Data Detail Penjualan Berhasil Ditambahkan!')
        return redirect('read_penjualan')
    

def update_detail_penjualan(request, id) :
    komoditas = models.komoditas.objects.all()
    produk = models.produk.objects.all()
    getpenjualan = models.penjualan.objects.all()
    getdetailpenjualan = models.detailpenjualan.objects.get(iddetail_penjualan = id)
    id_penjualan = getdetailpenjualan.id_penjualan.id_penjualan
    id_produk = getdetailpenjualan.id_produk.id_produk
    id_komoditas = getdetailpenjualan.id_komoditas.id_komoditas
    kuantitasp = getdetailpenjualan.kuantitas_produk
    kuantitask = getdetailpenjualan.kuantitas_komoditas

    print(id_penjualan)
    if request.method == 'GET' :
        return render (request, 'penjualan/update_detail_penjualan.html', {
            'kuantitasp' : kuantitasp,
            'kuantitask' : kuantitask,
            'id_komoditas' : id_komoditas,
            'id_produk' : id_produk,
            'komoditas' : komoditas,
            'produk' : produk,
            'id_penjualan' : id_penjualan,
            'getdetailpenjualan' : getdetailpenjualan,
            'getpenjualan' : getpenjualan,

        })
    
    else :
        idpenjualan = request.POST['idpenjualan']
        kuantitasp = request.POST['kuantitasp']
        kuantitask = request.POST['kuantitask']
        produk = request.POST['produk']
        komoditas = request.POST['komoditas']

        getdetailpenjualan.iddetail_penjualan = getdetailpenjualan.iddetail_penjualan
        getdetailpenjualan.id_penjualan = models.penjualan.objects.get(id_penjualan = idpenjualan)
        getdetailpenjualan.id_produk = models.produk.objects.get(id_produk = produk)
        getdetailpenjualan.id_komoditas = models.komoditas.objects.get(id_komoditas = komoditas)
        getdetailpenjualan.kuantitas_produk = kuantitasp
        getdetailpenjualan.kuantitas_komoditas = kuantitask

        getdetailpenjualan.save()
        messages.success(request, "Data Detail Penjualan berhasil diperbarui!")

        return redirect('read_penjualan')
    

def delete_detail_penjualan(request, id) :
    getdetailpenjualan = models.detailpenjualan.objects.get(iddetail_penjualan = id)
    getdetailpenjualan.delete()
    messages.success(request, "Data Penjualan berhasil dihapus!")
    return redirect('read_penjualan')

'''CRUD PRODUK'''
def create_produk(request) :
    if request.method == 'GET' :
        return render(request, 'produk/create_produk.html')
    
    else :
        nama_produk = request.POST['nama_produk']
        satuan_produk = request.POST['satuan_produk']
        harga_produk = request.POST['harga_produk']

        produkobj = models.produk.objects.filter(nama_produk = nama_produk)
        if produkobj.exists() :
            messages.error(request, 'Nama Produk sudah ada!')
            return redirect('create_produk')

        
        models.produk(
            nama_produk = nama_produk,
            satuan_produk = satuan_produk,
            harga_produk = harga_produk,
        ).save()

        messages.success(request, 'Data Produk Berhasil Ditambahkan!')
        return redirect('read_produk')

def read_produk(request) :
    produkobj = models.produk.objects.all()
    if not produkobj.exists():
        messages.error(request, "Data Produk Tidak Ditemukan!")

    return render(request, 'produk/read_produk.html', {
        'produkobj' : produkobj
    })

def update_produk(request, id) :
    getproduk = models.produk.objects.get(id_produk = id)
    if request.method == 'GET' :
        return render(request, 'produk/update_produk.html', {
            'getproduk' : getproduk,
        })
    
    else :
        nama_produk = request.POST['nama_produk']
        satuan_produk = request.POST['satuan_produk']
        harga_produk = request.POST['harga_produk']

        produkobj = models.produk.objects.filter(nama_produk = nama_produk, satuan_produk = satuan_produk, harga_produk = harga_produk)
        if produkobj.exists() :
            messages.error(request, 'Data Produk sudah ada!')
            return redirect('create_produk')

        getproduk.id_produk = getproduk.id_produk
        getproduk.nama_produk = nama_produk
        getproduk.satuan_produk = satuan_produk
        getproduk.harga_produk = harga_produk

        getproduk.save()

        messages.success(request, "Data Produk berhasil diperbarui!")
        return redirect('read_produk')

def delete_produk(request, id) :
    getproduk = models.produk.objects.get(id_produk = id)
    getproduk.delete()

    messages.success(request, "Data Produk berhasil dihapus!")
    return redirect('read_produk')

'''CRUD KOMODITAS'''
def create_komoditas(request) :
    if request.method == 'GET' :
        return render(request, 'komoditas/create_komoditas.html')
    
    else :
        nama_grade = request.POST['nama_grade']
        nama_komoditas = request.POST['nama_komoditas']
        harga_beli = request.POST['harga_beli']
        harga_jual = request.POST['harga_jual']

        komoditasobj = models.komoditas.objects.filter(nama_komoditas = nama_komoditas, id_grade__nama_grade = nama_grade)
        if komoditasobj.exists() :
            messages.error(request, 'Nama Komoditas sudah ada!')

        else :
            models.komoditas(
                id_grade = models.grade.objects.get(nama_grade = nama_grade),
                nama_komoditas = nama_komoditas,
                harga_beli = harga_beli,
                harga_jual = harga_jual,
            ).save()
            messages.success(request, 'Data Komoditas Berhasil Ditambahkan!')

        return redirect('read_komoditas')

def read_komoditas(request) :
    komoditasobj = models.komoditas.objects.all()
    if not komoditasobj.exists():
        messages.error(request, "Data Komoditas Tidak Ditemukan!")

    return render(request, 'komoditas/read_komoditas.html', {
        'komoditasobj' : komoditasobj
    })

def update_komoditas(request, id) :
    getkomoditas = models.komoditas.objects.get(id_komoditas = id)
    if request.method == 'GET' :
        return render(request, 'komoditas/update_komoditas.html', {
            'getkomoditas' : getkomoditas,
        })
    
    else :
        nama_grade = request.POST['nama_grade']
        nama_komoditas = request.POST['nama_komoditas']
        harga_beli = request.POST['harga_beli']
        harga_jual = request.POST['harga_jual']

        komoditasobj = models.komoditas.objects.filter(nama_komoditas = nama_komoditas, id_grade__nama_grade = nama_grade, 
                                                       harga_beli = harga_beli, harga_jual = harga_jual)
        if komoditasobj.exists() :
            messages.error(request, 'Data Komoditas sudah ada!')

        getkomoditas.id_komoditas = getkomoditas.id_komoditas
        getkomoditas.id_grade = models.grade.objects.get(nama_grade = nama_grade)
        getkomoditas.nama_komoditas = nama_komoditas
        getkomoditas.harga_beli = harga_beli
        getkomoditas.harga_jual = harga_jual

        getkomoditas.save()

        messages.success(request, 'Data Komoditas berhasil diperbarui!')
        return redirect('read_komoditas')

def delete_komoditas(request, id) :
    getkomoditas = models.komoditas.objects.get(id_komoditas = id)
    getkomoditas.delete()

    messages.success(request, "Data komoditas berhasil dihapus!")
    return redirect('read_komoditas')

'''CRUD PASAR'''
def create_pasar(request) :
    if request.method == 'GET' :
        return render(request, 'pasar/create_pasar.html')
    
    else :
        nama_pasar = request.POST['nama_pasar']
        alamat_pasar = request.POST['alamat_pasar']

        pasarobj = models.pasar.objects.filter(nama_pasar = nama_pasar)
        if pasarobj.exists() :
            messages.error(request, 'Nama Pasar sudah ada!')

        else :
            models.pasar(
                nama_pasar = nama_pasar,
                alamat_pasar = alamat_pasar,
            ).save()
            messages.success(request, 'Data Pasar Berhasil Ditambahkan!')

        return redirect('read_pasar')

def read_pasar(request) :
    pasarobj = models.pasar.objects.all()
    if not pasarobj.exists():
        messages.error(request, "Data Pasar Tidak Ditemukan!")

    return render(request, 'pasar/read_pasar.html', {
        'pasarobj' : pasarobj
    })

def update_pasar(request, id) :
    getpasar = models.pasar.objects.get(id_pasar = id)
    if request.method == 'GET' :
        return render(request, 'pasar/update_pasar.html', {
            'getpasar' : getpasar,
        })
    
    else :
        nama_pasar = request.POST['nama_pasar']
        alamat_pasar = request.POST['alamat_pasar']

        getpasar.id_pasar = getpasar.id_pasar
        getpasar.nama_pasar = nama_pasar
        getpasar.alamat_pasar = alamat_pasar

        getpasar.save()

        messages.success(request, 'Data Pasar berhasil diperbarui!')
        return redirect('read_pasar')

def delete_pasar(request, id) :
    getpasar = models.pasar.objects.get(id_pasar = id)
    getpasar.delete()

    messages.success(request, "Data pasar berhasil dihapus!")
    return redirect('read_pasar')



        

