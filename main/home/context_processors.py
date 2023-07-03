from .models import Page
from .forms import VinForm


def pages(request):
    return {'pages': Page.objects.filter(status=True)}



def vin_form(request):
    return {'vin_form': VinForm()}
