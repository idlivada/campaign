from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^^$', 'core.views.home', name='home'),
    url(r'^locator/', 'core.views.locator', name='locator'),
    url(r'^call/', 'core.views.call', name='call'),
    url(r'^dial-callback/', 'core.views.dial_callback', name='dial-callback'),
    url(r'^s/(?P<slug>[a-zA-Z0-9_.-]+)/', 'core.views.single_campaign', name='single-campaign'),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
