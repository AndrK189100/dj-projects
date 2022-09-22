from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sorting = request.GET.get('sort')
    template = 'catalog.html'
    if sorting == 'name':
        phones = Phone.objects.all().order_by('name')
    elif sorting == 'min_price':
        phones = Phone.objects.all().order_by('price')
    elif sorting == 'max_price':
        phones = Phone.objects.all().order_by('-price')
    else:
        phones = Phone.objects.all()

    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug)[0]

    context = {'phone': phone}
    return render(request, template, context)
