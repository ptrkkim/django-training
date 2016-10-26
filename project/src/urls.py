from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse

from src.core_auth.views import admin_login

urlpatterns = [
    url(r'^admin/login/$', admin_login),
    url(r'^admin/', admin.site.urls),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^api/', include('src.api.urls', namespace='api')),
    url(r'^auth/', include('src.core_auth.urls', namespace='core_auth')),
    url(r'^account/', include('src.core_auth.account_urls', namespace='account')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
