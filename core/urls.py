from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView,LogoutView
from . import views, urls, pds,tabla,tablaparch
from .views import HomePage

urlpatterns = [

    #Path del core
    path('',login_required(HomePage.as_view()), name="home"),
    path('file_upload', login_required(views.fileUpload), name='file_upload'),
    path('upload_csv', login_required(views.upload_csv), name='upload_csv'),
    path('save-config', login_required(views.InsertConfig), name='save-config'),
    path('tabla', login_required(tabla.makeTabla), name='tabla'),
    path('cor', login_required(tablaparch.makeCohCorr), name='cor'),
    path('pds', login_required(pds.makePds), name='pds'),
    path('get-config/<int:id>/<int:idA>', login_required(views.ConfigInicial), name='get-config')
    #path('plotSignal', views.plotSignal, name='plotSignal'),
    #path('get_data', views.get_data, name='get_data'),

]