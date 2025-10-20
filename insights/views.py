from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Region
from cart.models import Item
from movies.models import Movie

@login_required
def map_index(request):
    return render(request, 'insights/map.html', {
        'template_data': {'title':'Local Popularity Map'}
    })

@login_required
def regions_json(request):
    qs = Region.objects.all().values('id','name','lat','lng')
    return JsonResponse({'regions': list(qs)})

@login_required
def region_top_json(request, id):
    region = get_object_or_404(Region, id=id)
    # Aggregate Items via Order for this region
    rows = (Item.objects
        .filter(order__region=region)
        .values('movie__name')
        .annotate(total=Sum('quantity'))
        .order_by('-total')[:10])
    data = [{'title': r['movie__name'], 'count': r['total']} for r in rows]
    return JsonResponse({'region': region.name, 'top': data})
