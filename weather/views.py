from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse

from .forms import DbOperationsForm
from . import utils

from datetime import datetime
now = datetime.now()

# Create your views here.
def index(request):
    return render(request, 'home.html')

def data_visualization(request):
    if('reading_type' in request.GET.keys()):
        type = request.GET['reading_type']
    else:
        type = 'Tmax'
    if('year' in request.GET.keys()):
        year = int(request.GET['year'])
        if(year < 1910 or year > now.year):
            return render(request, 'present.html')
    else:
        year = now.year
    
    data = utils.present_overview(reading_type=type, year=year)
    data.sort()
    return render(request, 'present.html', {
                    'data' : data,
                    'reading_type' : type,
                    'year' : year,
                    'year_range' : range(1910,2018)
                    })

def db_operations(request):
    data = {}
    message = ''
    if request.method == 'POST':
        data = {}
        data['country'] = request.POST['country']
        data['reading_type'] = request.POST['reading_type']
        if('update' in request.POST.keys()):
            if(data['country'] == 'all'):
                if(data['reading_type'] == 'all'):
                    utils.updateDatabase()
                    message = "All latest values are updated!"
                else:
                    utils.updateDatabase(reading_types = [data['reading_type']])
                    message = "Database updated with latest values of " + data['reading_type']
            else:
                if(data['reading_type'] == 'all'):
                    utils.updateDatabase(countries = [data['country']])
                    message = "Database updated with latest values of " + data['country']
                else:
                    utils.updateDatabase(countries = [data['country']], reading_types = [data['reading_type']])
                    message = "Database updated with latest values of " + data['country'] + ' ' + data['reading_type']
                    
        elif('load' in request.POST.keys()):
            if(data['country'] == 'all'):
                if(data['reading_type'] == 'all'):
                    utils.loadDatabase()
                    message = "All latest values are updated!"
                else:
                    utils.loadDatabase(reading_types = [data['reading_type']])
                    message = "Database updated with latest values of " + data['reading_type']
            else:
                if(data['reading_type'] == 'all'):
                    utils.loadDatabase(countries = [data['country']])
                    message = "Database updated with latest values of " + data['country']
                else:
                    utils.loadDatabase(countries = [data['country']], reading_types = [data['reading_type']])
                    message = "Database updated with latest values of " + data['country'] + ' ' + data['reading_type']
                                                
    return render(request, 'data.html', {'data':data, 'message':message})

def about(request):
    return render(request, 'about.html')