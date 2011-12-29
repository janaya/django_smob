from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect, render, \
    get_object_or_404
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
#    logging.debug(request.user)
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
def person_edit(request): #, name=None):
    logging.debug("views.py person_edit")
    #if name:
    #    logging.debug("views.py person_edit, name")
    #    logging.debug(name)
    #    #person = get_object_or_404(Person, name=name)
    #    person = Person.objects.get()
    #    #if person != request.user:
    #    #    raise HttpResponseForbidden()
    #    logging.debug("views.py person_edit, person")
    #    logging.debug(person)
    #else:
    #    person = Person()
    try:
        person = Person.objects.get()
    except:
        person = Person()
    if request.method == 'POST':
        logging.debug("method post")
        form = PersonForm(request.POST, instance=person)
        formset = InterestFormSet(request.POST, instance=person)
        if form.is_valid() and formset.is_valid():
            logging.debug("form is valid")
            data = formset.cleaned_data
            logging.debug(data)
            person_instance = form.save()
            logging.debug(person_instance)
            formset.save()
            #formset = InterestFormSet(request.POST, 
            #                          instance = person_instance)
            #instances = formset.save(commit=False)
            #for instance in instances:
            #    instance.save()
            #if formset.is_valid():
            #   formset.save()
            if request.is_ajax():
                logging.debug("request ajax")
                response = {'status':True,}
                json = simplejson.dumps(response, ensure_ascii=False)
                return HttpResponse(json, mimetype="application/json")
#                return render(request, 'home')
            else:
                return redirect('home')
        else: # form no valid
            if request.is_ajax():
                logging.debug("request ajax")
                response = {'status':False,'errors':form.errors}
                json = simplejson.dumps(response, ensure_ascii=False)
                return HttpResponse(json, mimetype="application/json")
            else:
                logging.debug("form is not valid")

    else: # GET
        form = PersonForm(instance=person)
        formset = InterestFormSet(instance=person)
        logging.debug("method not post  ")
    return render_to_response('djsmob/person_edit.html', 
                               {'form': form, 'formset': formset,},
                               context_instance=RequestContext(request))

#@login_required
def post_add(request):
    logging.debug("views.py, post_add")
    if request.method == 'POST':
        logging.debug("method post")
        form = PostForm(request.POST)
        if form.is_valid():
            logging.debug("form is valid")
            content = form.cleaned_data['content']
            logging.debug(content)
            logging.debug(form.cleaned_data['location_uri'])
            post_instance = form.save(commit=False)
            logging.debug(post_instance.content)
            logging.debug(post_instance.location_uri)
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
                logging.debug("request ajax")
                response = {'status':True,}
                json = simplejson.dumps(response, ensure_ascii=False)
                return HttpResponse(json, mimetype="application/json")
#                return render(request, 'home')
            else:
                #return redirect('post_list')
                return HttpResponseRedirect(reverse('djsmob-post_list'))
        else: # form no valid
        
            if request.is_ajax():
                logging.debug("request ajax")
                response = {'status':False,'errors':form.errors}
                json = simplejson.dumps(response, ensure_ascii=False)
                return HttpResponse(json, mimetype="application/json")
            else:
              logging.debug("form is not valid")

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
    logging.debug(slug)
    if slug:
        post = Post.objects.filter(slug=slug)
        logging.debug(post)
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
