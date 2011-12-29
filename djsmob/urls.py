from django.conf.urls.defaults import *
from django.contrib.auth.views import User
from django.views.generic.simple import redirect_to
from django.views.generic import DetailView, ListView
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

#from models import *
from feeds import PostFeed, RDFPostFeed, XMLPostFeed

import logging

import os.path

#if os.path.isfile(settings.CONFIG_FILE):
#    default_view = "posts"
#else:
#    logging.debug("no config yet")
#    logging.debug(settings.CONFIG_FILE)
#    default_view = "config_add"

urlpatterns = patterns('djsmob.views',
    url(r'^$', 'posts', name='home'),
    #url(r'^config/add/$', 'config_add', name='djsmob-config_add'),
    url(r'^install/$', 'config_add', name='djsmob-install'),
    url(r'^person/$', 'person', name='djsmob-person'),
    url(r'^person/edit/$', 'person_edit', name='djsmob-person_edit'),
    #url(r'^person/edit/(?P<name>[-\w]+)/$', 'person_edit', name='djsmob-person_edit'),

    url(r'^post/add/$', 'post_add', name='djsmob-post_add'),
    url(r'^post/$', 
#        ListView.as_view(
#            model=Post,
##            queryset=Post.objects.order_by('-pub_date')[:10],
#            context_object_name='post_list',
##            template_name='post_list.html'), 
#        ),
        'posts',
        name='djsmob-post_list'),
    url(r'^post/(?P<slug>[-\w]+)/$',
#        DetailView.as_view(
#            model=Post,
##            template_name='post_detail.html'), 
#        ),
        'post',
        name='djsmob-post_detail'),
##
##    url(r'^json/post/$', 'posts_json', name='posts_json'),
##    url(r'^json/post/(?P<slug>[-\w]+)/$', 'post_json', name='post_json'),
##    
##    url(r'^data/me/$', 'person_rdf', name='person_rdf'),
)
urlpatterns += patterns('',
    (r'^rss/post/$', PostFeed()),
    (r'^rssrdf/post/$', RDFPostFeed()),#, name='djsmob-rssrdf'),
    (r'^xmlrdf/post/$', XMLPostFeed()),
)
urlpatterns += staticfiles_urlpatterns()

logging.debug("how many times is executed urls.py?")
