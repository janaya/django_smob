from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
#from django.contrib.auth.views import logout
from django.core import serializers
from django.conf import settings
from rdflib import URIRef, Namespace
import rdflib
from queries import query_posts
from models import *

FOAF=Namespace("http://xmlns.com/foaf/0.1/" )
#RDFS=Namespace("http://www.w3.org/2000/01/rdf-schema#")
SIOC=Namespace("http://rdfs.org/sioc/spec/")
SIOCT=Namespace("http://rdfs.org/sioc/types#")
DC=Namespace("http://purl.org/dc/elements/1.1/")
DCT=Namespace("http://purl.org/dc/terms/")
TAGS=Namespace("http://www.holygoat.co.uk/owl/redwood/0.1/tags/")
MOAT=Namespace("http://moat-project.org/ns#")
OPO=Namespace("http://online-presence.net/opo/ns#")
OPO_ACTIONS=Namespace("http://online-presence.net/OPO_ACTIONS/ns#")
CTAG=Namespace("http://commontag.org/ns#")
SMOB=Namespace("http://smob.me/ns#")
XSD=Namespace("http://www.w3.org/2001/XMLSchema#")
REV=Namespace("http://purl.org/stuff/rev#")
GEO=Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")

PUSH = Namespace("http://vocab.deri.ie/push/")
CERT = Namespace("http://www.w3.org/ns/auth/cert#")
RSA = Namespace("http://www.w3.org/ns/auth/rsa#")
REL = Namespace('http://purl.org/vocab/relationship/')


ns = dict(
          #rdfs=RDFS, 
          #rdf=RDF,
          rdf=Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
          rdfs=Namespace('http://www.w3.org/2000/01/rdf-schema#'),
         
          cert=CERT, 
          rsa=RSA,
          
          dc=DC,
          dct=DCT,
          
          foaf=FOAF, 
          
          sioc=SIOC,
          sioct=SIOCT,
          
          tags=TAGS,
          moat=MOAT,
          ctag=CTAG,
          
          opo=OPO,
          opo_actions=OPO_ACTIONS,
          
          smob=SMOB,
          push=PUSH, 
          
          xsd=XSD,
          rev=REV,
          geo=GEO)

#store = ConjunctiveGraph()
#store = rdflib.graph.Graph(settings.STORE)()

STORE = rdflib.plugin.get('SQLite', rdflib.store.Store)('smob.db')
try: 
    STORE.open('.', create=True) 
except:
    STORE.open('.', create=False)
##        logging.debug("store")
##        logging.debug(STORE)
store = rdflib.Graph(STORE)

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
        print "method not post  "
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
