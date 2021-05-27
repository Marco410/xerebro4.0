from django.shortcuts import render
import matplotlib.pyplot as plt
import pandas as pd
import io,csv,os,errno
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.http import HttpResponse, JsonResponse
import numpy as np
from scipy import signal
from scipy.signal import butter, lfilter 

def datosRaw(datos, init,endt,chanel):
    datosRaw=datos.loc[init:endt,chanel]
    return datosRaw

def butter_bandstop_filter(data, lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    i, u = butter(order, [low, high], btype='bandstop')
    y = lfilter(i, u, data)
    return y

def butter_bandpass(lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut/nyq
    high = highcut/nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a
    
def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

def graficar(csv_file, fs,init,ritmo,ednt,canales,user):
    fcL60=59      #Rechazo de ruido de la línea desde 59Hz hasta 61Hz
    fcH60=61
    fcA1=8        # Paso de frecuencias Alfa de 8 a 13Hz
    fcA2=13
    fcB1=13.5     # Paso de frecuencias Beta de 13.5 a 30Hz 
    fcB2=30
    fcT1=4        # Paso de frecuencias Tetha de 4 a 8Hz
    fcT2=8
    fcGL1=30      # Paso de frecuencias Gamma Bajas de 30 a 45Hz
    fcGL2=45 
    fcGH1=45      # Paso de frecuencias Gamma Altas de 45 a 100Hz 
    fcGH2=100
    orstop=4 #Orden del filtro rechazo de banda
    orpass=3 #Orden del filtro pasa banda 

    f = plt.figure()
    axes = f.add_axes([0.15, 0.15, 0.75, 0.75]) 
    print(canales)
    datos = pd.read_csv(csv_file,
                    delimiter='\t', #añadi un \ 
                    skiprows = 5,
                    usecols=range(0,14))
    datos.columns = ['CH{0:02d}'.format(i) for i in range(1,15)]
    datos.index = np.arange(0,datos.shape[0])/1024
    y =[]
    for x in range(len(canales)):
        print(canales[x])
        if(canales[x] == 'ch1'):
            data = datos.loc[0:3,"CH01"]
            data.shape
            y=butter_bandstop_filter(data, fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch2'):
            data = datos.loc[0:3,"CH02"]
            data.shape
            y=butter_bandstop_filter(data, fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch3'):
            data = datos.loc[0:3,"CH03"]
            data.shape
            y=butter_bandstop_filter(data, fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch4'):
            data = datos.loc[0:3,"CH04"]
            data.shape
            y=butter_bandstop_filter(data, fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch5'):
            data = datos.loc[0:3,"CH05"]
            data.shape
            y=butter_bandstop_filter(datos.loc[0:3,"CH05"], fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch6'):
            y=butter_bandstop_filter(datos.loc[0:3,"CH06"], fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch7'):
            y=butter_bandstop_filter(datos.loc[0:3,"CH07"], fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch8'):
            y=butter_bandstop_filter(datos.loc[0:3,"CH08"], fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch9'):
            y=butter_bandstop_filter(datos.loc[0:3,"CH09"], fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch10'):
            y=butter_bandstop_filter(datos.loc[0:3,"CH10"], fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch11'):
            y=butter_bandstop_filter(datos.loc[0:3,"CH11"], fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch12'):
            y=butter_bandstop_filter(datos.loc[0:3,"CH12"], fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch13'):
            y=butter_bandstop_filter(datos.loc[0:3,"CH13"], fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch14'):
            y=butter_bandstop_filter(datos.loc[0:3,"CH14"], fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch15'):
            y=butter_bandstop_filter(datos.loc[0:3,"CH15"], fcL60, fcH60, fs, orstop)
        elif(canales[x] == 'ch16'):
            y=butter_bandstop_filter(datos.loc[0:3,"CH16"], fcL60, fcH60, fs, orstop)
        #elif(canales[x] == 'ch17'):
            #plt.plot(datos.loc[0:3,'CH17'])
        #elif(canales[x] == 'ch18'):
            #plt.plot(datos.loc[0:3,'CH18'])            
            y.shape

    if (ritmo == "alfa"):
        yritmo=butter_bandpass_filter(y,fcA1,fcA2,fs,orpass)
    elif(ritmo == "beta"):
        yritmo=butter_bandpass_filter(y,fcB1,fcB2,fs,orpass)
    elif(ritmo == "gammaL"):
        yritmo=butter_bandpass_filter(y,fcGL1,fcGL2,fs,orpass)
    elif(ritmo == "gammaH"):
        yritmo=butter_bandpass_filter(y,fcGH1,fcGH2,fs,orpass)
    elif(ritmo == "theta"):
        yritmo=butter_bandpass_filter(y,fcT1,fcT2,fs,orpass)

    samples=len(yritmo)
    segSampled=samples
    freq= np.fft.fftfreq(samples)

    fftRitmo = np.fft.fft(yritmo)
    MagRitmo = abs(fftRitmo)

    freqNyq= int(samples/2)
    ejeFreq = np.arange(0,(fs/2))

    rango=len(ejeFreq)
    Tn=rango/freqNyq
    ejeFreqFinal=np.arange(0,rango,Tn)

    x=0
    MirrR = np.arange(freqNyq)
    for x in range(freqNyq):
        MirrR[x] = MagRitmo[x]

    plt.plot(ejeFreqFinal,MirrR)
    plt.xlim(0,120) 

    axes.set_xlabel("Tiempo")
    axes.set_ylabel("Cambios")

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)

    response = HttpResponse(buf.getvalue(), content_type='image/png')
    name = str(user)+ "/"+ str(csv_file)+str(canales)+ "signal.png"
    try:
        os.mkdir('core/static/core/senales/pds/'+str(user))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    f.savefig("core/static/core/senales/pds/"+name)

    return name

def makePds(request):
    
    if request.method == "GET":
        return render(request,"analisis/index.html")

    if request.method == "POST":    
    
        #csv_file = request.FILES
        filename = request.FILES.get('file_name',None)
        canal = request.POST.getlist('canal[]')
        fm = int(request.POST['fm_user'])
        ritmo = request.POST['ritmo']
        
        name = graficar(csv_file=filename,fs=fm,init=0,ritmo=ritmo,ednt=3,canales= canal,user=request.user.id)

        print(name)
        data = {
            'name': name
        }
        return JsonResponse(data)