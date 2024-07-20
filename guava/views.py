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
# Create your views here.


# CRUD MITRA
def read_mitra(request) :
    try :
        allmitra = models.mitra.objects.all()
        return render(request,
                      'mitra/read_mitra.html',
                      {
                          'allmitra' : allmitra
                      })
    except models.mitra.DoesNotExist :
        messages.error(request,"Data Mitra Tidak Ditemukan!")

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
            newmitra = models.mitra(
                nama_mitra = namamitra,
                alamat_mitra = alamatmitra,
                nohp_mitra = nohpmitra,
                tanggalawal_mitra = tanggalawalmitra,
                durasi_kontrak = durasikontrakmitra,
                luas_lahan = luaslahan,
                status_mitra = statusmitra
            )

            newmitra.save()
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