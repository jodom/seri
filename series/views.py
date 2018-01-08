from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    if request.method == 'POST':
        return HttpResponse(request.POST['serie'])
    return render(request, 'seris/home.html')
