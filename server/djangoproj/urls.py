from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),
    path('about', TemplateView.as_view(template_name='About.html')),
    path('contact', TemplateView.as_view(template_name='Contact.html')),
    re_path(r'^(?:|dealers/?|dealer/\d+/?|postreview/\d+/?|login/?|register/?)$',
            TemplateView.as_view(template_name='index.html')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
