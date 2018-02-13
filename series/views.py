from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import SerieForm, NoteForm
from .models import Serie, Note
# Create your views here.
def home(request):
    if request.method == 'POST':
        default_serie = Serie.objects.first()
        form = NoteForm(request.POST)
        if not default_serie or default_serie.title != 'My Notes':
            default_serie = Serie.objects.create(title='My Notes')
        note = form.save(commit=False)
        note.serie = default_serie
        note.save()
        return redirect('serie_detail', pk=default_serie.pk)
    else:
        form = NoteForm
        return render(request, 'series/home.html', {'form': form})

def new_serie(request):
    if request.method == 'POST':
        form = SerieForm(request.POST)
        serie = form.save()
        return redirect('serie_detail', pk=serie.pk)
    else:
        form = SerieForm
        return render(request, 'series/new_serie.html', {'form': form})

def serie_detail(request, pk=None):
    if pk:
        form = NoteForm
        serie = Serie.objects.get(id=pk)
        return render(request, 'series/serie.html', {'serie': serie, 'form': form})
    return render(request, 'series/serie.html')


def add_note(request, pk):
    pass
