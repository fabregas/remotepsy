from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from rempsy.views import *

urlpatterns = patterns('', url(r'^i18n/', include('django.conf.urls.i18n')),)

urlpatterns += i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^registration/$', registration),
    url(r'^activate_user/(.*)$', activate_user),
    url(r'^restore_password/$', restore_password),
    url(r'^set_password/(.*)$', set_password)
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
