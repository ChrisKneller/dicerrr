"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views
from dice import views as dice_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', dice_views.index, name='index'),
    path('admin/', admin.site.urls),
    path('create/', dice_views.AjaxUploadView.as_view(), name='upload'),
    path('tempuserify', dice_views.create_lazyuser_then_redirect, name='create_lazyuser'),
    # path('upload/<str:img_url>/', dice_views.image_transform, name='transform'),
    path('create/transform/', dice_views.image_transform, name='transform'),
    path('convert/', include('lazysignup.urls')),
    path('share/<str:image_id>', dice_views.image_share, name='share'),
    path('my-creations/', dice_views.my_uploads, name='my_uploads'),
    path('my-creations/<int:page>', dice_views.my_uploads, name='my_uploads'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = dice_views.error404
handler500 = dice_views.error404

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ]