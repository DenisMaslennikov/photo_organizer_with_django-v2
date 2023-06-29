from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from  django.conf import  settings


handler400 = 'pages.views.bad_request'
handler404 = 'pages.views.page_not_found'
handler403 = 'pages.views.forbidden'
handler500 = 'pages.views.server_error'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gallery.urls', namespace='gallery')),
    path('users/', include('users.urls', namespace='users')),
    path('', include('pages.urls', namespace='pages')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)), )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)