from django.conf.urls.defaults import *

urlpatterns = patterns('djlod.views',
    url(r'^dbpedia/(?P<term>[-\w]+)/$', 'dbpedia_candidates', name='djlod-dbpedia_candidates'),
    url(r'^sindice/(?P<term>[-\w]+)/$', 'sindice_candidates', name='djlod-sindice_candidates'),
    url(r'^geo/(?P<term>[-\w]+)/$', 'geo_candidates', name='djlod-geo_candidates'),
    url(r'^term/(?P<term>[-\w]+)/$', 'term_candidates', name='djlod-term_candidates'),
)
