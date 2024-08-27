from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.conf import settings

from actions.utils import create_action

from .forms import ImageCreateForm
from .models import Image
from .utils import create_redis_connection


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image added successfully')
            return redirect(new_image.get_absolute_url())
        else:
            messages.error(request, 'image was not added. something went wrong.')
    else:
        form = ImageCreateForm(data=request.GET)
    return render(
        request,
        'images/create.html',
        {'section': 'images', 'form': form}
    )


@login_required
def image_detail(request, image_id, slug):
    img = get_object_or_404(Image, id=image_id, slug=slug)
    # connet to the redis sever r
    r = create_redis_connection(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)

    # increment total image views by one
    total_views = r.incr(f'image: {img.id}: views')
    # increment image ranking by 1
    r.zincrby('image_ranking', 1, img.id)
    return render(request, 'images/detail.html', {'image': img, 'total_views': total_views})


@require_POST
@login_required()
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 10)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:

        if images_only:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(request, 'images/list_images.html', {'section': 'images', 'images': images})
    ctx = {'images': images, 'section': 'images'}
    return render(request, 'images/list.html', context=ctx)


@login_required
def image_ranking(request):
    r = create_redis_connection(settings.REDIS_HOST, settings.REDIS_PORT, settings.REDIS_DB)
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_rakning_ids = [int(id) for id in image_ranking]
    #     get the most view images
    most_viewed = list(Image.objects.filter(
        id__in=image_rakning_ids
    ))
    most_viewed.sort(key=lambda x: image_rakning_ids.index(x.id))
    return render(request, 'images/ranking.html', {'section': 'images', 'most_viewed': most_viewed})
