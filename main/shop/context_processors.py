from .models import Category, ShopSetup, Manufacturer

def categorys(request):
    return {'categorys': Category.objects.filter(parent=None, status=True, top=True).order_by('sort_order')}


def manufacts(request):

    return {'manufacts': Manufacturer.objects.all().order_by('name')}
