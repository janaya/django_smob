from django.conf.urls.defaults import *
from django.contrib.auth.views import User
from django.views.generic.simple import redirect_to
from django.views.generic import DetailView, ListView
from django.views.generic.simple import direct_to_template

from models import *

urlpatterns = patterns('djsmob.views',
    url(r'^me/$', 'person', name='djsmob-person'),
##    url(r'^me/edit/$', 'person_edit', name='person_edit'),

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
