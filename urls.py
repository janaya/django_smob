from django.conf.urls.defaults import patterns, include, url
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_smob2.views.home', name='home'),
    url(r'^', include('django_smob2.djsmob.urls')),
    url(r'^lod/', include('django_smob2.djlod.urls')),

    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
#urlpatterns += staticfiles_urlpatterns()

#if settings.SERVE_MEDIA:
#    urlpatterns += patterns("",
#        url(r"", include("staticfiles.urls")),
#    )
