from django.shortcuts import render
from .models import Service, ServSetup

# Create your views here.
def serv(request):

    servs = Service.objects.all()
    
    context = {
        'servs': servs,
        'serv_setup': ServSetup.objects.get()
    }
    
    return render(request, 'serv/serv.html', context)



def serv_detail(request, slug):

    serv = Service.objects.get(slug=slug)

    context = {
        'serv': serv
    }
    
    return render(request, 'serv/serv_detail.html', context)