from django.urls import path

from . import views

app_name = 'gallery'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path(
        'tag/<slug:tag_slug>/',
        views.TagImageListView.as_view(),
        name='tag_view',
    ),
    path(
        'photo-by/<str:model>/',
        views.PhotoByListView.as_view(),
        name='photo_by',
    ),

    path(
        'user/<str:username>/',
        views.UserImageListView.as_view(),
        name='user_profile',
    ),
    path('image/<int:pk>', views.ImageDetailView.as_view(), name='image'),
    path(
        'image/<int:pk>/add-comment',
        views.AddCommentCreateView.as_view(),
        name='add_comment',
    ),
    path(
        'image/<int:pk>/update',
        views.ImageUpdateView.as_view(),
        name='update_image',
    ),
    path('add-image/', views.ImageCreateView.as_view(), name='add_image'),
    path('add-tag/', views.add_tag, name='add_tag'),
    path('search/', views.SearchListView.as_view(), name='search')
]
