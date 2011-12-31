from django.conf.urls.defaults import *

urlpatterns = patterns('djlod.views',
    url(r'^dbpedia/$', 'dbpedia_candidates', name='djlod-dbpedia_candidates'),
    url(r'^dbpedia/(?P<term>[-\w]+)/$', 'dbpedia_candidates', name='djlod-dbpedia_candidates'),
    url(r'^sindice/(?P<term>[-\w]+)/$', 'sindice_candidates', name='djlod-sindice_candidates'),
    url(r'^geo/$', 'geo_candidates', name='djlod-geo_candidates'),
    url(r'^geo/(?P<term>[-\w]+)/$', 'geo_candidates', name='djlod-geo_candidates'),
    url(r'^geo/html/$', 'html_geo_candidates', name='djlod-html_geo_candidates'),
    url(r'^term/html/$', 'html_term_candidates', name='djlod-html_term_candidates'),
    url(r'^term/html/(?P<term>[-\w]+)/$', 'html_term_candidates', name='djlod-html_term_candidates'),
)
