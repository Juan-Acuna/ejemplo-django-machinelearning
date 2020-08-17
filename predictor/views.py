from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Atributo, Calidad
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from django_pandas.io import read_frame
from sklearn.cluster import KMeans

forest  = RandomForestRegressor(random_state=69)
kmeans = KMeans(n_clusters = 5, init = "k-means++",random_state = 46)

def Inicio(request):
    return render(request, 'inicio.html')

def Predict(request):
    respuesta = HttpResponse()
    test = Calidad.objects.all()
    if(len(test)<=0):
        respuesta.write("<div id='rc'class='r-cont'><h4>No hay datos iniciados para realizar la operacion</h4><p>Por favor haga click <a href='/insert' onclick='Gif()'>aqui</a> para inicializar</p>")
        respuesta.write("<p>Esto podria tardar hasta un minuto.</p></div>")
        return respuesta
    Reload()
    a = request.GET['a']
    b = request.GET['b']
    c = request.GET['c']
    pred = forest.predict([[a,b,c]])
    atr = Atributo(v_acidity = a, r_sugar = b, alcohol = c)
    atr.save()
    q = Calidad(quality = pred)
    q.save()
    pred2 = PredictKMeans()
    respuesta.write("<div id='rc'class='r-cont'><h4>Valores ingresados</h4>")
    respuesta.write("<p><b>Volatile acidity: </b>{}</p>".format(str(a)))
    respuesta.write("<p><b>Residual sugar: </b>{}</p>".format(str(b)))
    respuesta.write("<p><b>Alcohol: </b>{}</p>".format(str(c)))
    respuesta.write("<br><h3><b>Calidad obtenida: {}</b></h3></div>".format(str(pred[0])))
    respuesta.write("<div id='kc'class='k-cont'>")
    respuesta.write("<h4>Valores ingresados</h4>")
    respuesta.write("<p><b>Volatile acidity: </b>{}</p>".format(str(a)))
    respuesta.write("<p><b>Residual sugar: </b>{}</p>".format(str(b)))
    respuesta.write("<p><b>Alcohol: </b>{}</p><br>".format(str(c)))
    respuesta.write("<h3><b>Calidad obtenida: {}</b></h3></div>".format(str(pred2[-1])))
    return respuesta

def Reload():
    atrib = read_frame(Atributo.objects.all(), fieldnames=['v_acidity','r_sugar','alcohol'])
    cal   = read_frame(Calidad.objects.all(), fieldnames=['quality'])
    at2   = np.array(atrib[["v_acidity","r_sugar","alcohol"]])
    cal2  = np.array(cal.quality)
    x_train, x_test, y_train, y_test = train_test_split(at2, cal2, test_size = 0.2, random_state=42)
    forest.fit(x_train,y_train)

def PredictKMeans():
    atrib = read_frame(Atributo.objects.all(), fieldnames=['v_acidity','r_sugar','alcohol'])
    at2   = np.array(atrib[["v_acidity","r_sugar","alcohol"]])
    km = kmeans.fit_predict(at2)
    return km

#METODOS DE UN SOLO USO
def Insert(request):
    data  = pd.read_csv("http://127.0.0.1:8000/static/data/winequality-red.csv",sep=";")
    x = np.array(data[["volatile acidity","residual sugar","alcohol"]])
    y = np.array(data.quality)
    for i in range(0,1596):
        atr = Atributo(v_acidity = x[i,0], r_sugar = x[i,1], alcohol = x[i,2])
        atr.save()
        q = Calidad(quality = y[i])
        q.save()
    return HttpResponseRedirect('/postinsert')

def postinsert(request):
    atr = Atributo.objects.all()
    q   = Calidad.objects.all()
    return render(request, 'postinsert.html', {'calidad': q,'atributo':atr})

