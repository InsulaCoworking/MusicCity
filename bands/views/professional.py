import random

from django.shortcuts import render, get_object_or_404

from bands.models import Professional


def pro_list(request):

    pros = list(Professional.objects.all())
    random.shuffle(pros)
    return render(request, 'professional/list.html', {
        'pros': pros
    })

def pro_detail(request, pk):
    pro = get_object_or_404(Professional, pk=pk)
    return render(request, 'professional/detail.html', {
        'pro': pro,
        'view': request.GET.get('view', None)
    })
