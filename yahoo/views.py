from django.shortcuts import render
from .models import Category
from django.db import connection
from django.http import JsonResponse
from django.http import HttpResponse
import json

# Create your views here.

def interface(request):
    categories = Category.objects.all()
    return render(request,
    'interface.html',
    # {'categories': categories}
    )

def query(request):
    if request.method == 'POST':
        query = request.POST['query']
        cursor = connection.cursor()
        result = cursor.execute(query).fetchall()
        json_result = json.dumps(result)
        decode_result = json.loads(json_result)
        # print(json_result)

        return JsonResponse(decode_result, safe=False)
