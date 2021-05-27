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

def makeCohCorr(request):

    if request.method == "POST":    
    
        #csv_file = request.FILES
        canal = request.POST.getlist('canal[]')
        fm = int(request.POST['fm_user'])
        condicion = request.POST['condicion']

        chanel=canal[0]
        Ch1A,Ch1B,Ch1T,Ch1GL,Ch1GH=procesar(request=request,condicion=condicion,canal=chanel, fs=fm)
        chanel=canal[1]
        Ch2A,Ch2B,Ch2T,Ch2GL,Ch2GH=procesar(request=request,condicion=condicion,canal=chanel, fs=fm)
        # COHERENCIA

        ch1Ritmo = np.array([Ch1A,Ch1B,Ch1T,Ch1GL,Ch1GH])
        ch2Ritmo = np.array([Ch2A,Ch2B,Ch2T,Ch2GL,Ch2GH])

        data = {}
        data['coherencia'] =[]
        data['correlacion'] =[]

        for x in range(len(ch1Ritmo)):
            f, Cxy = signal.coherence(ch1Ritmo[x], ch2Ritmo[x])
            f=np.delete(f,0)
            Cxy=np.delete(Cxy,0)
            Coh=np.mean(Cxy)
            Coh
            data['coherencia'].append(Coh)
            #CORRELACIÓN
            corrPar=pearsonr(ch1Ritmo[x], ch2Ritmo[x])
            corrPar=corrPar[0]
            corrPar
            data['correlacion'].append(corrPar)

            print(data)

        return JsonResponse(data)

def read_file(request,init,endt,canal,fs):
    configActiva = Config_User.objects.get(active=1,user_id=request.user.id)
        
    datos = pd.read_csv(configActiva.file_name,
                    delimiter='\t', 
                    skiprows = 5,
                    usecols=range(0,configActiva.ncanales))
    FNCanales = configActiva.ncanales + 1
    datos.columns = ['CH{0:02d}'.format(i) for i in range(1,FNCanales)]
    datos.index = np.arange(0,datos.shape[0])/fs
    return datos.loc[init:endt,canal]

def datosRaw(request,condicion,canal,fs):
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
    if(canal == 'ch1'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH01', fs=fs)
    elif(canal == 'ch2'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH02', fs=fs)
    elif(canal == 'ch3'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH03', fs=fs)
    elif(canal == 'ch4'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH04', fs=fs)
    elif(canal == 'ch5'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH05', fs=fs)
    elif(canal == 'ch6'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH06', fs=fs)
    elif(canal == 'ch7'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH07', fs=fs)
    elif(canal == 'ch8'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH08', fs=fs)
    elif(canal == 'ch9'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH09', fs=fs)
    elif(canal == 'ch10'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH10', fs=fs)
    elif(canal == 'ch11'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH11', fs=fs)
    elif(canal == 'ch12'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH12', fs=fs)
    elif(canal == 'ch13'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH13', fs=fs)
    elif(canal == 'ch14'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH14', fs=fs)
    elif(canal == 'ch15'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH15', fs=fs)
    elif(canal == 'ch16'):
        datosRaw= read_file(request=request,init=init,endt=endt,canal='CH16', fs=fs)
    
    return datosRaw 

def butter_bandstop_filter(data, lowcut, highcut, fs, order):
        nyq = 0.5 * fs
        low = lowcut / nyq
        high = highcut / nyq
        i, u = butter(N=order, Wn=[low, high], btype='bandstop')
        y = lfilter(b=i, a=u, x=data)
        return y

def butter_bandpass(lowcut, highcut, fs, order): 
    nyq = 0.5 * fs 
    low = lowcut/nyq 
    high = highcut/nyq 
    b, a = butter(N=order, Wn=[low, high], btype='band') 
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5): 
    b, a = butter_bandpass(lowcut=lowcut, highcut=highcut, fs=fs, order=order) 
    y = signal.filtfilt(b, a, data,axis=0) 
    return y

def procesar(request,condicion,canal,fs):
    
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
    orstop=4 
    orpass=3

    datosIn=datosRaw(request=request,condicion=condicion,canal=canal,fs=fs)
    y=butter_bandstop_filter(data=datosIn,lowcut=fcL60,highcut=fcH60,fs=fs,order=orstop) #Se Filtra el Canal del Ruido de la Línea 
    y.shape

    yAlfa=butter_bandpass_filter(data=y,lowcut=fcA1,highcut=fcA2,fs=fs,order=orpass)
    yBeta=butter_bandpass_filter(data=y,lowcut=fcB1,highcut=fcB2,fs=fs,order=orpass)
    yGammaL=butter_bandpass_filter(data=y,lowcut=fcGL1,highcut=fcGL2,fs=fs,order=orpass)
    yGammaH=butter_bandpass_filter(data=y,lowcut=fcGH1,highcut=fcGH2,fs=fs,order=orpass)
    yTheta=butter_bandpass_filter(data=y,lowcut=fcT1,highcut=fcT2,fs=fs,order=orpass)

    return yAlfa,yBeta,yTheta,yGammaL,yGammaH

