from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
import json
from lod_candidates.candidates import *

def dbpedia_candidates(request, term=None):
    if not term: term = request.GET.get('q')
    candidates = get_dbpedia_candidates(term)
    return HttpResponse(json.dumps(candidates), mimetype="application/json")

def sindice_candidates(request, term):
    candidates = get_sindice_candidates(term)
    return HttpResponse(json.dumps(candidates), mimetype="application/json")

def geo_candidates(request, term=None):
    if not term: term = request.GET.get('q')
    candidates = get_geo_candidates(term)
    return HttpResponse(json.dumps(candidates), mimetype="application/json")

def html_geo_candidates(request,term=None):
    if not term: term = request.GET.get('q')
    candidates = get_geo_candidates(term)
    return render_to_response('djlod/geo_candidates.html', 
                               {'term': term,
                               'candidates': candidates,
                               },
                               context_instance=RequestContext(request))
                               
def html_term_candidates(request,term=None):
    if not term: term = request.GET.get('q')
    dbpedia_candidates = get_dbpedia_candidates(term)
    sindice_candidates = get_sindice_candidates(term)
    return render_to_response('djlod/term_candidates.html', 
                               {'term': term,
                               'dbpedia_candidates': dbpedia_candidates,
                               'sindice_candidates': sindice_candidates,
                               },
                               context_instance=RequestContext(request))
    
