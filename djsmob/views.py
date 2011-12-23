from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
#from django.contrib.auth.views import logout
from django.core import serializers
from django.conf import settings

import logging

from models import *
from forms import *
from namespaces import *

def person(request):
#    print request.user
#    profile = request.user.get_profile()
    person = request.user.profile
    #profile = request.META['USER']
    return render_to_response('djsmob/me.html', {'person':person},
                               context_instance=RequestContext(request))

def person_rdf(request):
    person = Person.objects.all()[0]
    return HttpResponse(content=person.to_rdf(),
                        content_type='application/rdf+xml')

#@login_required
def person_edit(request):
    if request.method == 'POST':
        print "method post"
        form = PersonForm(request.POST)
        if form.is_valid():
            print "form is valid"
            person_instance = form.save()
            
            if request.is_ajax():
                print "request ajax"
                response = {'status':True,}
                json = simplejson.dumps(response, ensure_ascii=False)
                return HttpResponse(json, mimetype="application/json")
#                return render(request, 'home')
            else:
                return redirect('home')
        else: # form no valid
            if request.is_ajax():
                print "request ajax"
                response = {'status':False,'errors':form.errors}
                json = simplejson.dumps(response, ensure_ascii=False)
                return HttpResponse(json, mimetype="application/json")
            else:
                print "form is not valid"

    else: # GET
        form = PersonForm()
        print "method not post  "
    return render_to_response('djsmob/person_edit.html', {'form': form,},
                               context_instance=RequestContext(request))

#@login_required
def post_add(request):
    logging.debug("views.py, post_add")
    if request.method == 'POST':
        print "method post"
        form = PostForm(request.POST)
        if form.is_valid():
            print "form is valid"
            content = form.cleaned_data['content']
            print content
            post_instance = form.save(commit=False)
            #post_instance.creator = request.user.profile
            #post_instance.creator = request.META['USER'].profile
            # hackish
            #post_instance.creator = Person.objects.get(name='duy')
            #post_instance.creator = Person.objects.filter(user__username = 'duy')[0]
            post_instance.save()
            print post_instance.content 
            
            if request.is_ajax():
                print "request ajax"
                response = {'status':True,}
                json = simplejson.dumps(response, ensure_ascii=False)
                return HttpResponse(json, mimetype="application/json")
#                return render(request, 'home')
            else:
                #return redirect('post_list')
                return HttpResponseRedirect(reverse('djsmob-post_list'))
        else: # form no valid
        
            if request.is_ajax():
                print "request ajax"
                response = {'status':False,'errors':form.errors}
                json = simplejson.dumps(response, ensure_ascii=False)
                return HttpResponse(json, mimetype="application/json")
            else:
              print "form is not valid"

    else: # GET
        form = PostForm()
        logging.debug("method not post")
        logging.debug(form)
    return render_to_response('djsmob/post_add.html', {'form': form,},
                               context_instance=RequestContext(request))

def posts(request):
    posts = Post.objects.all()
    return render_to_response('djsmob/post_list.html', 
                               {'post_list': posts,},
                               context_instance=RequestContext(request))
                               
def post(request, slug):
    post = Post.objects.get(slug)
    return render_to_response('djsmob/post_detail.html', 
                               {'post': post,},
                               context_instance=RequestContext(request))
def posts_json(request):
    posts = Post.objects.all()
    return HttpResponse(serializers.serialize('json', posts), mimetype="application/json")
    return HttpResponse()

def post_json(request, slug):
#    slug = request.GET.get("post_slug")
    print slug
    if slug:
        post = Post.objects.filter(slug=slug)
        print post
        return HttpResponse(serializers.serialize('json', post), mimetype="application/json")
    return HttpResponse()
