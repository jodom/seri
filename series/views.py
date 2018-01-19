from django.shortcuts import render, redirect
from django.http import HttpResponse

from . import forms
from . import models
# Create your views here.
def home(request):
    return render(request, 'series/home.html')

def new_serie(request):
    if request.method == 'POST':
        form = forms.SerieForm(request.POST)
        serie = form.save()
        return redirect('serie_detail', pk=serie.pk)
        # return render(request, 'series/serie.html', {'serie_title': serie.title})
    else:
        form = forms.SerieForm
        return render(request, 'series/new_serie.html', {'form': form})

def serie_detail(request, pk):
    serie = models.Serie.objects.get(id=pk)
    return render(request, 'series/serie.html', {'serie_title': serie.title})
