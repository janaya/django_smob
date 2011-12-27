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
        formset = InterestFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            print "form is valid"
            data = formset.cleaned_data
            print data
            person_instance = form.save()
            print person_instance
            formset.save()
            #formset = InterestFormSet(request.POST, 
            #                          instance = person_instance)
            #instances = formset.save(commit=False)
            #for instance in instances:
            #    instance.save()
            #if formset.is_valid():
            #   formset.save()
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
        formset = InterestFormSet()
        print "method not post  "
    return render_to_response('djsmob/person_edit.html', 
                               {'form': form, 'formset': formset,},
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
            print form.cleaned_data['location_uri']
            post_instance = form.save(commit=False)
            print post_instance.content 
            print post_instance.location_uri
            #post_instance.creator = request.user.profile
            #post_instance.creator = request.META['USER'].profile
            # hackish
            #post_instance.creator = Person.objects.get(name='duy')
            #post_instance.creator = Person.objects.filter(user__username = 'duy')[0]
            
            #location_formset = LocationFormSet(request.POST, instance=post_instance)
            #if location_formset.is_valid():
            #    post_instance.save()
            #    location_formset.save() 
            
            post_instance.save()
            
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
        #location_formset = LocationFormSet(instance=Post())
    return render_to_response('djsmob/post_add.html', {
                              'form': form,
                              #"location_formset": location_formset,
                            }, context_instance=RequestContext(request))

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
    return HttpResponse(serializers.serialize('json', posts), 
                        mimetype="application/json")
    return HttpResponse()

def post_json(request, slug):
#    slug = request.GET.get("post_slug")
    print slug
    if slug:
        post = Post.objects.filter(slug=slug)
        print post
        return HttpResponse(serializers.serialize('json', post), 
                            mimetype="application/json")
    return HttpResponse()

def config_add(request):
    #logging.debug("request path")
    #logging.debug(request.path)
    #logging.debug(request.META['HTTP_REFERER'] )
    #logging.debug("http://"+request.get_host() + request.get_full_path())
    #logging.debug(request.build_absolute_uri())
    if request.method == 'POST':
        logging.debug("method post")
        form = ConfigurationForm(request.POST)
        if form.is_valid():
            configuration_instance = form.save()
            logging.debug("configuration file saved")
            h = Hub.objects.get()
            logging.debug("hub: ")
            logging.debug(h)
            if not h:
                h = Hub()
                h.save()
                logging.debug("hub: ")
                logging.debug(h)
            return redirect('djsmob-person_edit')
            #return render(request, 'home')
            #return redirect('post_list')
            #return HttpResponseRedirect(reverse('djsmob-post_list'))
        else: 
            logging.debug("form is not valid")

    else: # GET
        form = ConfigurationForm()
        logging.debug("method not post  ")
    return render_to_response('djsmob/config_add.html', 
                               {'form': form},
                               context_instance=RequestContext(request))
