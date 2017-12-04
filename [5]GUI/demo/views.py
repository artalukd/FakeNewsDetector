# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect
from gui_function import predict  

def index(request):
    if request.method == "POST":
        text = request.POST['article']
        #headline = request.POST['header']
        header =""
        prediction = predict(header,text)
        
        if prediction > 0.5:
            label = "Real"
        else:
            label = "Fake"
        
        return render(request, 'demo/tail.html', {'prediction': prediction, 'label': label})
    else:
        return render(request, 'demo/head.html')
