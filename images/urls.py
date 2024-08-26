from django.urls import path

from . import views

app_name = 'images'

urlpatterns = [
    path('create/', views.image_create, name='create'),
    path('<int:image_id>/<slug:slug>/detail/', views.image_detail, name='detail')
]
