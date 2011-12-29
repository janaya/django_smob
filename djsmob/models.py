#!/usr/bin/python
# vim: set expandtab tabstop=4 shiftwidth=4:
# -*- coding: utf-8 -*-
#
# This file is part of androsmob
#
# androsmob is distributed under the terms of the BSD License. The full license is in
# the file LICENSE, distributed as part of this software.
#
# Copyright (c) 2011, Digital Enterprise Research Institute (DERI),NUI Galway.
# All rights reserved.
#
# Author: Julia Anaya
# Email: julia dot anaya at gmail dot com
#
# FILE:
# models.py
#
# DESCRIPTION:
#
# TODO:

from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.conf import settings

from datetime import datetime

import logging

from urlparse import urlparse

from rdflib import Literal, BNode, ConjunctiveGraph, Graph, RDF, RDFS
import rdflib

from namespaces import *
from queries import *

#logger = logging.getLogger('django_smob')

logging.debug("how many times is executed models.py?")

# verion>=3
#STORE = rdflib.graph.Graph(settings.STORE)()

STORE_DB  = rdflib.plugin.get('SQLite', rdflib.store.Store)(settings.STORE_DB_NAME)
try: 
    r = STORE_DB.open(settings.STORE_DB_PATH, create=True) 
    logging.debug('store_db')
    logging.debug(r)
    # bind namespaces only when created
    [STORE.bind(*x) for x in NS.items()]
except:
    r = STORE_DB.open('.', create=False)
    logging.debug('store_db')
    logging.debug(r)
STORE = rdflib.Graph(STORE_DB)
#STORE = ConjunctiveGraph(STORE_DB)
#g= ConjunctiveGraph(STORE_DB, Namespace('http://localhost:8000')
#http://xmppwebid.github.com/xmppwebid/julia
#[STORE.bind(*x) for x in NS.items()]

class HubManager(models.Manager):
    def get(self):
        hub = None
        q = query_select_hub
        r = STORE.query(q, initNs=NS)
        for instance in r:
            logging.debug('HubManager.get() instance')
            logging.debug(instance)
            #?site_uri, ?site_rss, ?foaf_doc_uri
            site_uri = instance[0]
            rss_url = instance[1]
            foaf_doc_uri = instance[2]
            hub = Hub(site_uri = str(site_uri), 
                    foaf_doc_uri = str(foaf_doc_uri),
                    rss_url = rss_url)
        return hub

class Hub(models.Model):
    site_uri = models.URLField(_('Site URI'), default=str(SITE_URI))
    foaf_doc_uri = models.URLField(_('FOAF Doc URI'), 
                                    default=str(FOAF_DOC_URI))
    rss_url = models.URLField(_('RSS URI'), default=str(RSS_URI))
    objects = HubManager()

    def __unicode__(self):
        return self.site_uri
        
    def rdf(self):
        rdf = """?site_uri a push:SemanticHub . 
            ?site_rss push:has_hub ?site_uri .
            ?site_rss push:has_owner ?foaf_doc_uri . 
            """ % (URIRef(self.site_uri).n3(), 
        URIRef(self.rss_url).n3(), URIRef(self.site_uri).n3(), 
        URIRef(self.rss_url).n3(), URIRef(self.foaf_doc_uri).n3())
        logging.debug('Hub.rdf(), rdf')
        logging.debug(rdf)
        return rdf
        
    def to_graph(self):
        g = Graph(STORE_DB)
        g.add((URIRef(self.site_uri), RDF.type, PUSH['SemanticHub']))
        g.add((URIRef(self.rss_url), PUSH['has_hub'],
                URIRef(self.site_uri)))
        g.add((URIRef(self.rss_url), PUSH['has_owner'],
                URIRef(self.foaf_doc_uri)))
        rdf=g.serialize(format="nt")
        logging.debug('Hub.to_rdf(), rdf')
        logging.debug(rdf)
        return g
    
    def insert_query(self):
        rdf = self.rdf()
        q = query_insert_into_graph_triples % (HUB_URI, rdf)
        logging.debug("query")
        logging.debug(q)
        r = STORE.query(q, initNs=NS)
        logging.debug("result insert query")
        logging.debug(r)
    
    def save(self, *args, **kwargs):
        #g = self.to_graph()
        #g.commit()
        self.insert_query()
        
class InterestQuerySet(QuerySet):
    def get(self, label=None): 
        logging.debug("InterestQuerySet.get")
        if label:
            interest = None
            q = query_interest % Literal(label).n3()
            r = STORE.query(q, initNs=NS)
            for instance in r:
                logging.debug('InterestManager.all() instance')
                logging.debug(instance)
                
                person = Person.objects.get()
                uri = str(instance[0])
                interest = Interest(uri = uri, 
                            label = label, person = person)
            return interest
        else:
            interests = []
            q = query_interests
            r = STORE.query(q, initNs=NS)
            for instance in r:
                logging.debug('InterestManager.all() instance')
                logging.debug(instance)
                
                uri = str(instance[0])
                label = str(instance[1])
                person = Person.objects.get()
                interest = Interest(uri = uri, 
                            label = label, person = person)
                interests.append(interest)
            return interests

    def ordered(self):
        logging.debug("InterestQuerySet.ordered")
        return False
    
    def __getattr__(self, attr, *args):
        logging.debug("InterestQuerySet.__getattr__")
        return getattr(self.get_query_set(), attr, *args)
    
    def  filter(self, *args, **kwargs):
        logging.debug("InterestQuerySet.filter")
        #kwargs = {person: p}
        return self.get()
    
class InterestManager(models.Manager):
        
    def get_query_set(self):
        logging.debug("InterestManager.get_query_set")
        return InterestQuerySet(self.model)

class Interest(models.Model):
    uri = models.URLField(_('interest uri'), )
    label = models.CharField(_('interest label'),max_length=255)
    person = models.ForeignKey('Person',)
    objects = InterestManager()
    
    def __unicode__(self):
        return self.label

    def save(self, *args, **kwargs):
        self.to_rdf()
        STORE.commit()
        
    def to_rdf(self):
        uri = URIRef(self.uri)
        STORE.add((FOAF_URI, FOAF['topic_interest'], uri))
        STORE.add((uri, RDFS.label, Literal(self.label)))
        rdf=STORE.serialize(format="nt")
        logging.debug('Interest.to_rdf(), rdf')
        logging.debug(rdf)
        return rdf

class PersonManager(models.Manager):
    def all(self):
        persons = []
        #uris = [p for p in STORE.subjects(RDF.type, FOAF["Person"])]
        #for uri in uris:
        persons.append(self.get())
        return persons
    
    def get(self, name=None):
        #uri = [s for s in STORE.subjects(RDF.type, FOAF["Person"])][0]
        #name = [o for o in STORE.objects(URIRef(uri), FOAF["nickname"])][0]
        #p = self.model(User.objects.all()[0], name)
        #return p
        person = None
        q = query_select_person % (FOAF_URI.n3(), FOAF_URI.n3())
        r = STORE.query(q, initNs=NS)
        for instance in r:
            logging.debug('PersonManager.get() instance')
            logging.debug(instance)
            #uri, container, content, created, title, reply_of, 
            #reply_of_of, presence, location, locname = instance
            name = str(instance[0])
            person = Person(name = name)
        logging.debug("PersonManager.get, person")
        logging.debug(person)
        return person


class Person(models.Model):
    #user = models.ForeignKey(User, unique=True)
    #user = OneToOneField(User)
    name = models.CharField(max_length=100, # default='anonymous',
                           blank=True) # , null=True
    # depiction
    #interests = models.ManyToManyField(Interest)
    #relationships
    objects = PersonManager()

    @models.permalink
    def get_absolute_url(self):
        return ('djsmob-person')
    #    return "/me/"
    #    return ('djsmob.views.person')
    #    return('person')

#    def uri(self):
#        return "%s%s" % (self.get_absolute_url(), self.created) 
        
    #models.permalink
    def uri(self):
        return self.get_absolute_url()
        #return "/person/"
        #return ('person', [])
        #return ('djsmob.views.person')
        #return ('djsmob-person')
        #return FOAF

    def __unicode__(self):
        #return unicode(self.user.username)
        return self.name

    def save(self, *args, **kwargs):
##        if not self.user:
##            # hackish
##            self.user = User.objects.all()[0]
##            if not self.name:
##                self.name = self.user.username
##        #super(Person, self).save(*args, **kwargs)
        self.to_rdf()
        STORE.commit()

##    def from_graph(self):
####        graph.parse(data=foaf, format=parsers[content_type])
##        self.name = [p for p in STORE.subjects(RDF.type, FOAF["Person"])]

    def to_rdf(self):
        STORE.add((FOAF_URI, RDF.type, FOAF["Person"]))
        STORE.add((FOAF_DOC_URI, RDF.type, FOAF['PersonalProfileDocument']))
        STORE.add((FOAF_URI, FOAF['maker'], FOAF_URI))
        STORE.add((FOAF_URI, FOAF['primaryTopic'], FOAF_URI))
        STORE.add((FOAF_URI, FOAF['nickname'],Literal(self.name)))
        # if foar_uri != me_uri
        # STORE.add((uri, RDFS['seeAlso'],foaf_uri))
        
##        cert = BNode()
##        STORE.add((cert, RDF.type, RSA['RSAPublicKey']))
##        STORE.add((cert, CERT['identity'], person_uri))
##    
##        modulus = BNode()
##        STORE.add((cert, RSA['modulus'], modulus))
##        STORE.add((modulus, CERT['hex'], Literal(person_orm.modulus)))
##        
##        exponent = BNode()
##        STORE.add((cert, RSA['public_exponent'], exponent))
##        STORE.add((exponent, CERT['decimal'], Literal(person_orm.public_exponent)))
##        STORE.commit()

        rdf=STORE.serialize(format="pretty-xml", max_depth=1)
        return rdf

#User.profile = property(lambda u: Person.objects.get_or_create(user=u)[0])

class Relationship(models.Model):
    uri = models.URLField(_('relationship'), )
    label = models.CharField(_('label'),max_length=255)

    def __unicode__(self):
        return self.label
    
#class Knows(models.Model):
#    from_person = models.ForeignKey(Person)
#    to_person = models.ForeignKey(Person)
#    type_rel = models.ForeignKey(Relationship)

class Location(models.Model):
    uri = models.URLField(_('location'), )
    label = models.CharField(_('label'),max_length=255)

    def __unicode__(self):
        return self.label

class PostManager(models.Manager):
    def all(self):
        posts = []
        #uris = [p for p in STORE.subjects(RDF.type, SIOC["Post"])]
        #for uri in uris:
        #    posts.append(self.get(uri))
        q = query_posts % SITE_URI.n3()
        r = STORE.query(q, initNs=NS)
        for instance in r:
            #uri, container, content, created, title, reply_of, 
            #reply_of_of, presence, location, locname = instance
            logging.debug('PostManager.all() instance')
            logging.debug(instance)
            
            uri = instance[0]
            container = instance[1]
            content = instance[2]
            created = instance[3]
            title = instance[4]
            reply_of = instance[5]
            reply_of_of = instance[6]
            presence = instance[7]
            location_uri = instance[8]
            location_label = instance[9]
            post = Post(slug = uri.replace(str(POST_URI),''), 
                        title = title,
                        content= content, created=created, 
                        reply_of = reply_of, 
                        location_label = location_label,
                        location_uri = location_uri)
            posts.append(post)
        return posts
            
    def get(self, slug):
        #uri = [s for s in STORE.subjects(RDF.type, FOAF["Person"])][0]
        #name = [o for o in STORE.objects(URIRef(uri), FOAF["nickname"])][0]
        #p = self.model(User.objects.all()[0], name)
        #return p
        #FIXME: hackish
        post = None
        uri = URIRef(POST_URI+slug).n3()
        q = query_post % uri
        r = STORE.query(q, initNs=NS)
        for instance in r:
            logging.debug('PostManager.get() instance')
            logging.debug(instance)
            #uri, container, content, created, title, reply_of, 
            #reply_of_of, presence, location, locname = instance
            container = instance[0]
            content = instance[1]
            created = instance[2]
            title = instance[3]
            reply_of = instance[4]
            reply_of_of = instance[5]
            presence = instance[6]
            location_uri = instance[7]
            location_label = instance[8]
            post = Post(slug = slug, title = title,
                        content= content, created=created, 
                        reply_of = reply_of,
                        location_label = location_label,
                        location_uri = location_uri)
        return post

class Post(models.Model):
    #uri = models.URLField(_(''), default=''+self.created, editable=False)
    slug = models.SlugField(unique=True, editable=False)
    title = models.CharField(_('title'), max_length=140, editable=False)
    content = models.CharField(_('content'), max_length=140)
    created = models.DateTimeField(_('sent'), default=datetime.now, editable=False)
    #reply_of = models.URLField(_(''), default='', editable=False)
    reply_of = models.ForeignKey('Post', blank=True, null=True)
    #location = models.ForeignKey(Location, blank=True, null=True)
    location_uri = models.URLField(_('location uri'), blank=True, null=True)
    location_label = models.CharField(_('location'), max_length=140, blank=True, null=True)
    
#    has_creator = models.URLField(_(''), default='', editable=False)
    creator = models.ForeignKey(Person, related_name='creator_of', editable=False)
#    maker = models.URLField(_(''), default='', editable=False)

#    has_container= models.URLField(_(''), default=SITE_URL, editable=False)
#    opo_uri= models.URLField(_(''), default=self.uri+'#presence', editable=False)
    objects = PostManager()

    @models.permalink
    def get_absolute_url(self):
        return ('djsmob-post_detail', [str(self.slug)])

    def uri(self):
        return URIRef(POST_URI+self.slug)

    #@models.permalink
    def has_container(self):
        return SITE_URI

    #@models.permalink
    def has_creator(self):
        return self.creator.uri()

    #@models.permalink
    def maker(self):
        return self.has_creator()+'#id'

    #@models.permalink
    def opo_uri(self):
        return self.has_creator()+'#presence'

    def __unicode__(self):
        #return self.uri
        #return "%s%s" % (self.permalink, self.created) 
        return self.get_absolute_url()

    def save(self, *args, **kwargs):
        #if not self.id:
        self.slug = slugify(self.created)
            #self.has_creator=self.has_creator
        self.title = 'Updated - '+self.content
        #super(Post, self).save(*args, **kwargs)
        logging.debug('Post.save() slug')
        logging.debug(self.slug)
        self.to_rdf()
        STORE.commit()

    def to_rdf(self):
        #STORE = ConjunctiveGraph()
        
        #namespaces
        [STORE.bind(*x) for x in NS.items()]
        
        #FIXME: hackish
        #post_uri = self.uri()
        #print self.uri()
        #AttributeError: 'Post' object has no attribute 'uri'
        post_uri = URIRef(POST_URI+self.slug)
        STORE.add((SITE_URI, RDF.type, SMOB["Hub"]))
        STORE.add((post_uri, RDF.type, SIOCT["MicroblogPost"]))
        STORE.add((post_uri, SIOC["has_container"], URIRef(self.has_container())))
        
        STORE.add((post_uri, DCT["created"], Literal(self.created))) 
        #',datatype=_XSD_NS.date) 
        #STORE.add((post_uri, SIOC["has_creator"], URIRef(self.has_creator())))
        #STORE.add((post_uri, FOAF["maker"], URIRef(self.maker())))
        
        STORE.add((post_uri, SIOC["content"], Literal(self.content)))
        STORE.add((post_uri, DCT["title"], Literal(self.title)))
        if self.reply_of:
            STORE.add((post_uri, SIOC["reply_of"], URIRef(self.reply_of.uri())))
        
        #opo_uri = URIRef(self.opo_uri())
        #FIXME: hackish
        opo_uri = URIRef("http://localhost:8000/me#presence")
        #STORE.add((opo_uri, RDF.type, OPO["OnlinePresence"]))
        #STORE.add((opo_uri, OPO["declaredOn"], URIRef(self.has_creator())))
        #STORE.add((opo_uri, OPO["declaredBy"], URIRef(self.maker())))
        #STORE.add((opo_uri, OPO["StartTime"], Literal(self.created)))
        #STORE.add((opo_uri, OPO["customMessage"], post_uri))
        
        if self.location_label and self.location_uri:
            STORE.add((opo_uri, OPO["currentLocation"], URIRef(self.location_uri)))
            STORE.add((URIRef(self.location_uri), RDFS.label, Literal(self.location_label)))
        #STORE.add(())
        

        rdf=STORE.serialize(format="nt", max_depth=1)
        logging.debug('Post.to_rdf(), rdf')
        logging.debug(rdf)
        return rdf


    def to_rdf_graph(self):
        g = ConjunctiveGraph()
        post_uri = URIRef(POST_URI+self.slug)
        g.add((SITE_URI, RDF.type, SMOB["Hub"]))
        g.add((post_uri, RDF.type, SIOCT["MicroblogPost"]))
        g.add((post_uri, SIOC["has_container"], URIRef(self.has_container())))
        
        g.add((post_uri, DCT["created"], Literal(self.created))) 
        #',datatype=_XSD_NS.date) 
        #g.add((post_uri, SIOC["has_creator"], URIRef(self.has_creator())))
        #g.add((post_uri, FOAF["maker"], URIRef(self.maker())))
        
        g.add((post_uri, SIOC["content"], Literal(self.content)))
        g.add((post_uri, DCT["title"], Literal(self.title)))
        if self.reply_of:
            g.add((post_uri, SIOC["reply_of"], URIRef(self.reply_of.uri())))
        
        #opo_uri = URIRef(self.opo_uri())
        #g.add((opo_uri, RDF.type, OPO["OnlinePresence"]))
        #g.add((opo_uri, OPO["declaredOn"], URIRef(self.has_creator())))
        #g.add((opo_uri, OPO["declaredBy"], URIRef(self.maker())))
        #g.add((opo_uri, OPO["StartTime"], Literal(self.created)))
        #g.add((opo_uri, OPO["customMessage"], post_uri))
        
        if self.location:
            g.add((opo_uri, OPO["currentLocation"], URIRef(self.location_uri)))
            g.add((URIRef(self.location_uri), RDFS.label, Literal(self.location_label)))
        #g.add(())
        
        rdf=g.serialize(format="nt")
        logging.debug('Post.to_rdf_graph(), rdf')
        logging.debug(rdf)
        return rdf


    def rdf(self):
        uri = URIRef(POST_URI+self.slug).n3()
        q = query_post_rdf % (uri, uri)
        r = STORE.query(q, initNs=NS)
        rdf = r.result.serialize(format='nt')
        logging.debug('Post.rdf(), rdf')
        logging.debug(rdf)
        return rdf

class ConfigurationManager(models.Manager):
    def get(self):
        from config import *
        c = Configuration(site_url = SITE_URL, hub_url = HUB_URL, 
            hub_publish_url = HUB_PUBLISH_URL, 
            hub_subscribe_url = HUB_SUBSCRIBE_URL, 
            websocket_host = WEBSOCKET_HOST,
            websocket_port =  WEBSOCKET_PORT)
        return c
        

class Configuration(models.Model):
    #djdb = models.CharField(_('Django DB'), default="dev.db", max_length=255)
    #storedb = models.CharField(_('Django DB'), default="smob.db", max_length=255)
    site_url = models.URLField(_('Site URL'), default='http://localhost:8000')
    hub_url = models.URLField(_('Hub URL'), default='http://localhost:8080')
    hub_publish_url = models.URLField(_('Hub Publish URL'), default='http://localhost:8080/publish')
    hub_subscribe_url = models.URLField(_('Hub Subscribe URL'), default='http://localhost:8080/subscribe')
    websocket_host =  models.CharField(_('Websocket Host'), default='localhost', max_length=255)
    websocket_port =  models.IntegerField(_('Websocket Port'), default=8081)
    external_foaf_uri = models.URLField(_('External FOAF URI'), blank=True, null=True)

    def save(self, *args, **kwargs):
        data = """SITE_URL = "%s"
HUB_URL = "%s"
HUB_PUBLISH_URL = "%s"
HUB_SUBSCRIBE_URL = "%s"
WEBSOCKET_HOST = "%s"
WEBSOCKET_PORT = "%s"
EXTERNAL_FOAF_DOC = "%s" """ % (
        self.site_url, self.hub_url, self.hub_publish_url, 
        self.hub_subscribe_url, self.websocket_host, 
        self.websocket_port,
        self.external_foaf_uri)
        f = open(settings.CONFIG_FILE,'w')
        f.write(data)
        f.close()
