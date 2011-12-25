from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
import json
from lod_candidates.candidates import *

def dbpedia_candidates(request, term):
    candidates = get_dbpedia_candidates(term)
    return HttpResponse(json.dumps(candidates), mimetype="application/json")

def sindice_candidates(request, term):
    candidates = get_sindice_candidates(term)
    return HttpResponse(json.dumps(candidates), mimetype="application/json")

def geo_candidates(request, term):
    candidates = get_geo_candidates(term)
    return HttpResponse(json.dumps(candidates), mimetype="application/json")

def term_candidates(request,term):
    dbpedia_candidates = get_dbpedia_candidates(term)
    sindice_candidates = get_sindice_candidates(term)
    return render_to_response('djlod/term_candidates.html', 
                               {'term': term,
                               'dbpedia_candidates': dbpedia_candidates,
                               'sindice_candidates': sindice_candidates,
                               },
                               context_instance=RequestContext(request))
    