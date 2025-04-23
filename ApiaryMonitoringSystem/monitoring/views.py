from django.shortcuts import render
import json
import os
from django.http import JsonResponse
from .utils import *


    
def index(request):
    data = get_measurements()
    return render(request, 'index.html', {'data': data})

# Create your views here.
