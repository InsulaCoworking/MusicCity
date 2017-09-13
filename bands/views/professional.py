import random

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from bands.models import Professional, ProfessionalTag


def pro_list(request):

    pro_list = Professional.objects.all()
    paginator = Paginator(pro_list, 4)
    page = request.GET.get('page')
    try:
        pros = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pros = paginator.page(1)
    except (EmptyPage, InvalidPage):
        # If page is out of range (e.g. 9999), deliver last page of results.
        pros = paginator.page(paginator.num_pages)

    if request.is_ajax():
        pass
    else:
        tags = ProfessionalTag.objects.all()
        return render(request, 'professional/list.html', {
            'pros': pros, 'tags':tags, 'filtered_tags':None, 'page':page
        })

def pros_map_info(request):

    venues = Professional.objects.all().order_by('-latitude').select_related('tag').values('pk', 'name', 'latitude', 'longitude', 'profile_image', 'tag__name', 'tag__color')
    data = list(venues)
    return JsonResponse(data, safe=False, content_type="application/json")

def pro_detail(request, pk):
    pro = get_object_or_404(Professional, pk=pk)
    return render(request, 'professional/detail.html', {
        'pro': pro,
        'view': request.GET.get('view', None)
    })
