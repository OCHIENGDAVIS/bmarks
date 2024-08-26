from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .forms import ImageCreateForm
from .models import Image


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
    return render(request, 'images/detail.html', {'image': img})


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
