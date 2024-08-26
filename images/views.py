from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
