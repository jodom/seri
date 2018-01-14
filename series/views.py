from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'series/home.html')

def new_serie(request):
    if request.method == 'POST':
        return render(request, 'series/serie.html', {'serie_title': request.POST['serie']})
    return render(request, 'series/serie.html')
