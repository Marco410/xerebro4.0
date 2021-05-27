from .models import Config_User,User,TablesUser
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, JsonResponse
import io,csv,os,errno
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from numpy import array
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView



class HomePage(TemplateView):
    template_name = "analisis/index.html"
    
    def get(self, request,*args,**kwargs):
        c = suma(a=1,b=4)
        configs = Config_User.objects.all()
        configs = Config_User.objects.filter(user_id=request.user.id)
        tables = TablesUser.objects.all()
        tables = TablesUser.objects.filter(user_id=request.user.id)
        try:
            configActiva = Config_User.objects.get(active=1,user_id=request.user.id)
        except Config_User.DoesNotExist:
            configActiva = ""
        return render(request, self.template_name,{'image':'default.png','result':c,'configs':configs,'tables':tables,'activa':configActiva} )

def InsertConfig(request):
    if request.method == "GET":
        return render(request,"analisis/index.html")

    if request.method == "POST":
        try:
            find = Config_User.objects.get(active=1,user_id=request.user.id)
            find.active = 0
            find.save()
        except Config_User.DoesNotExist:
            print("Todo bien")
        name = request.POST['name_c']
        file_name = request.FILES['file_name']
        ncanales = int(request.POST['no_canales'])
        canales = request.POST.getlist('ch[]')
        ch = ""
        for x in range(len(canales)):
            print(canales[x])
            ch += canales[x]+ ","
        data = {
            'file_name':file_name,
            'ncanales':ncanales,
            'name':name,
            'canales':ch
            }
        
        if(name != ""):
            #con los ** se convierte a un objeto de tipo Config_User
            config = Config_User(user=request.user,**data)
            config.save()

        data2 = {
            'name':name,
            'canales':ch
        }
        return JsonResponse(data2)

def ConfigInicial(request,*args, **kwargs):
    try:
        if kwargs['id'] != kwargs['idA']:
            if kwargs['id'] != 0:
                config = Config_User.objects.get(id=kwargs['id'],user_id=request.user.id)
                data = {
                'id': config.id,
                'canales':config.canales,
                'v':True
                }
                config.active = 1
                config.save()
                print("Entro a id != 0")
                if kwargs['idA'] != 0:
                    config2 = Config_User.objects.get(id=kwargs['idA'],user_id=request.user.id)
                    config2.active = 0
                    config2.save()
                    print("Entro idA != 0")
        else:
            config = Config_User.objects.get(id=kwargs['id'],user=request.user.id)
            data = {
            'id': config.id,
            'canales':config.canales,
            'v':True
            }
            print("Entro a que son iguales")

        return JsonResponse(data)    
    except Config_User.DoesNotExist:
        data = {
            'v': False
        }
        return JsonResponse(data)

def suma(a,b):
    c = a + b
    return c

def fileUpload(request):
    fileName= request.FILES.get('file_name',None)
    return fileName

def dataFile(csv_file2, inicio, final,canal):
    datos = pd.read_csv(csv_file2,
                    delimiter='\t', 
                    skiprows = 5,
                    usecols=range(0,14))
    datos.columns = ['CH{0:02d}'.format(i) for i in range(1,15)]
    datos.index = np.arange(0,datos.shape[0])/1024
    return datos.loc[1:3,canal]


def graficar(csv_file, canales,user):

    f = plt.figure()
    axes = f.add_axes([0.15, 0.15, 0.75, 0.75]) 
    print(canales)
    datos = pd.read_csv(csv_file,
                    delimiter='\t', 
                    skiprows = 5,
                    usecols=range(0,14))
    datos.columns = ['CH{0:02d}'.format(i) for i in range(1,15)]
    datos.index = np.arange(0,datos.shape[0])/1024
    for x in range(len(canales)):
        print(canales[x])
        if(canales[x] == 'ch1'):
            plt.plot(datos.loc[0:3,"CH01"])
        elif(canales[x] == 'ch2'):
            plt.plot(datos.loc[0:3,"CH02"])
        elif(canales[x] == 'ch3'):
            plt.plot(datos.loc[0:3,"CH03"])
        elif(canales[x] == 'ch4'):
            plt.plot(datos.loc[0:3,"CH04"])
        elif(canales[x] == 'ch5'):
            plt.plot(datos.loc[0:3,"CH05"])
        elif(canales[x] == 'ch6'):
            plt.plot(datos.loc[0:3,"CH06"])
        elif(canales[x] == 'ch7'):
            plt.plot(datos.loc[0:3,"CH07"])
        elif(canales[x] == 'ch8'):
            plt.plot(datos.loc[0:3,"CH08"])
        elif(canales[x] == 'ch9'):
            plt.plot(datos.loc[0:3,"CH09"])
        elif(canales[x] == 'ch10'):
            plt.plot(datos.loc[0:3,"CH10"])
        elif(canales[x] == 'ch11'):
            plt.plot(datos.loc[0:3,"CH11"])
        elif(canales[x] == 'ch12'):
            plt.plot(datos.loc[0:3,"CH12"])
        elif(canales[x] == 'ch13'):
            plt.plot(datos.loc[0:3,"CH13"])
        elif(canales[x] == 'ch14'):
            plt.plot(datos.loc[0:3,"CH14"])
        elif(canales[x] == 'ch15'):
            plt.plot(datos.loc[0:3,"CH15"])
        elif(canales[x] == 'ch16'):
            plt.plot(datos.loc[0:3,"CH16"])
        #elif(canales[x] == 'ch17'):
            #plt.plot(datos.loc[0:3,'CH17'])
        #elif(canales[x] == 'ch18'):
            #plt.plot(datos.loc[0:3,'CH18'])            
    
    axes.set_xlabel("Tiempo")
    axes.set_ylabel("Cambios")

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    response = HttpResponse(buf.getvalue(), content_type='image/png')
    name = str(user)+ "/"+ str(csv_file)+str(canales)+ "signal.png"
    try:
        os.mkdir('core/static/core/senales/'+str(user))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    f.savefig("core/static/core/senales/"+name)

    return name

def upload_csv(request):

    if request.method == "GET":
        return render(request,"analisis/index.html")

    if request.method == "POST":    
    
        #csv_file = request.FILES
        filename = request.FILES.get('file_name',None)
        canal = request.POST.getlist('canal[]')
        fm = int(request.POST['fm_user'])
        
        name = graficar(csv_file=filename,canales= canal,user=request.user.id )

        print(name)
        data = {
            'name': name
        }
        return JsonResponse(data)#, {'data':signalA, 'label':t})

