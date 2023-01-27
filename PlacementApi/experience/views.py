from django.shortcuts import render,HttpResponse
import pandas as pd
from .models import * 
# Create your views here.

def roll_filling(request):
    if request.method == 'GET':
        data = pd.read_csv("roles.txt",header=None,names = ['role'])
        # print(data)
        for index, row in data.iterrows():
            new_role = Role(role = row["role"])
            new_role.save()
        return HttpResponse("hii")

        

