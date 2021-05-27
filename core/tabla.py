import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
from scipy.signal import butter, lfilter 
from scipy.signal import freqz
from scipy import signal 
import statistics as stats
import io,csv,os,errno,json
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Config_User

def butter_bandstop_filter(data, lowcut, highcut, fm, order):
        nyq = 0.5 * fm
        low = lowcut / nyq
        high = highcut / nyq
        i, u = butter(N=order, Wn=[low, high], btype='bandstop')
        y = lfilter(b=i, a=u, x=data)
        return y

def butter_bandpass(lowcut, highcut, fm, order): 
    nyq = 0.5 * fm 
    low = lowcut/nyq 
    high = highcut/nyq 
    b, a = butter(N=order, Wn=[low, high], btype='band') 
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fm, order=5): 
    b, a = butter_bandpass(lowcut=lowcut, highcut=highcut, fm=fm, order=order) 
    y = signal.filtfilt(b, a, data,axis=0) 
    return y

def makeTabla(request):
    
    if request.method == "GET":
        return render(request,"analisis/index.html")

    if request.method == "POST":    
    
        #filename = request.FILES.get('file_name',None)
        fm = int(request.POST['fm_user'])
        condicion = request.POST['condicion']
        configActiva = Config_User.objects.get(active=1,user_id=request.user.id)
        
        tabla = calcularTabla(Ncanales=configActiva.ncanales,request=request,condicion=condicion,fm=fm)
        data = {
            'tabla': tabla
        }
        return HttpResponse(tabla)

def read_file(request,init,endt,canal,fm):

    configActiva = Config_User.objects.get(active=1,user_id=request.user.id)
        
    datos = pd.read_csv(configActiva.file_name,
                    delimiter='\t', 
                    skiprows = 5,
                    usecols=range(0,configActiva.ncanales))
    FNCanales = configActiva.ncanales + 1
    datos.columns = ['CH{0:02d}'.format(i) for i in range(1,FNCanales)]
    datos.index = np.arange(0,datos.shape[0])/fm
    return datos.loc[init:endt,canal]


def datosRaw(request,condicion,canal,fm):
    init=0
    endt=0
    if(condicion == "1"):
        init = 21
        endt = 82
    elif (condicion =="2"):
        init = 88
        endt = 148
    elif(condicion == "9"):
        init = 676
        endt = 737
    datosRaw= read_file(request=request,init=init,endt=endt,canal=canal,fm=fm)
    
    return datosRaw 

def procesar(request,condicion,fm,canal):
    
    fcL60=59   
    fcH60=61
    fcA1=8
    fcA2=13
    fcB1=13.5
    fcB2=30
    fcT1=4 
    fcT2=8
    fcGL1=30 
    fcGL2=45 
    fcGH1=45
    fcGH2=100
    orstop=4 #Orden del filtro rechazo de banda
    orpass=3
    datosIn=datosRaw(request=request,condicion=condicion,canal=canal,fm=fm)
    y=butter_bandstop_filter(data=datosIn,lowcut=fcL60,highcut=fcH60,fm=fm,order=orstop) #Se Filtra el Canal del Ruido de la Línea 
    y.shape

    yAlfa=butter_bandpass_filter(data=y,lowcut=fcA1,highcut=fcA2,fm=fm,order=orpass)
    yBeta=butter_bandpass_filter(data=y,lowcut=fcB1,highcut=fcB2,fm=fm,order=orpass)
    yGammaL=butter_bandpass_filter(data=y,lowcut=fcGL1,highcut=fcGL2,fm=fm,order=orpass)
    yGammaH=butter_bandpass_filter(data=y,lowcut=fcGH1,highcut=fcGH2,fm=fm,order=orpass)
    yTheta=butter_bandpass_filter(data=y,lowcut=fcT1,highcut=fcT2,fm=fm,order=orpass)
    
    segment=fm/2
    ovlap=segment/2

    fA, Pxx_A = signal.welch(yAlfa,window='hamming',nperseg=segment,fs=fm,scaling='density',average='median',noverlap=ovlap)
    fB, Pxx_B = signal.welch(yBeta,window='hamming',nperseg=segment,fs=fm,scaling='density',average='median',noverlap=ovlap)
    fT, Pxx_T = signal.welch(yTheta,window='hamming',nperseg=segment,fs=fm,scaling='density',average='median',noverlap=ovlap)
    fGL, Pxx_GL = signal.welch(yGammaL,window='hamming',nperseg=segment,fs=fm,scaling='density',average='median',noverlap=ovlap)
    fGH, Pxx_GH = signal.welch(yGammaH, window='hamming',nperseg=segment,fs=fm,scaling='density',average='median',noverlap=ovlap)

    PDSA=Pxx_A.sum()
    PDSB=Pxx_B.sum()
    PDST=Pxx_T.sum()
    PDSGL=Pxx_GL.sum()
    PDSGH=Pxx_GH.sum()

    PDSprom=np.array([[PDSA],[PDSB],[PDST],[PDSGL],[PDSGH]])
    return PDSprom
    

def calcularTabla(Ncanales,request,condicion,fm):
    j=0
    n=['CH{0:02d}'.format(j) for j in range(1,Ncanales+1)]

    PDSprom=np.empty(shape=[5,1])
    matrix=np.empty(shape=[Ncanales-1,5,1])
    matrix=PDSprom
    i=0
    for i in range(Ncanales):    
        chanel=n[i]
        PDSfinal=procesar(request=request,condicion=condicion,fm=fm,canal=chanel)
        matrix=np.append(matrix,PDSfinal,axis=1)
    Columnas=Ncanales+1
    matrixFinal=np.delete(matrix,0,1)

    configActiva = Config_User.objects.get(active=1,user_id=request.user.id)
    cabeceraList = configActiva.canales.split(sep=",")
    cabecera=[cabeceraList]
    print(cabeceraList.pop()) #no mover!!, elimina el index demás
    df=pd.DataFrame(matrixFinal)
    df.columns=cabecera
    df.index=['Alfa','Beta','Theta','GammaBaja','GammaAlta']
    return df.to_html(classes="table table-dark table-striped table-responsive table-hover",table_id="pds-table")
    



        