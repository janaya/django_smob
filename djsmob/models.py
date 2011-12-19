from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.conf import settings
from urlparse import urlparse
from rdflib import URIRef, Literal, BNode, Namespace, ConjunctiveGraph, RDF, RDFS
from rdflib import Namespace
import rdflib
from queries import query_posts, query_post
import logging
logger = logging.getLogger('django_smog')

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


NS = dict(
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



#STORE = ConjunctiveGraph()
#STORE = rdflib.graph.Graph(settings.STORE)()

STORE_DB  = rdflib.plugin.get('SQLite', rdflib.store.Store)('smob.db')
try: 
    STORE_DB.open('.', create=True) 
except:
    STORE_DB.open('.', create=False)
##        logging.debug("STORE")
##        logging.debug(STORE)
STORE = rdflib.Graph(STORE_DB)

SITE_URI = URIRef(settings.SITE_URL)
FOAF_DOC_URI = URIRef(settings.SITE_URL + "/me")
FOAF_URI = URIRef(settings.SITE_URL + "/me#id")
POST_URI = URIRef(settings.SITE_URL + "/data/post/")
FOLLOWINGS_URI = URIRef(settings.SITE_URL + "/data/followings")
PRIVACY_PREFERENCES_URI = URIRef(settings.SITE_URL + "/data/privacy_preferences")
PRIVACY_PREFERENCE_URI = URIRef(settings.SITE_URL + "data/privacy_preference/")
OPO_URI = URIRef(settings.SITE_URL + "/me#presence")



class PersonManager(models.Manager):
    def all(self):
        persons = []
        uris = [p for p in STORE.subjects(RDF.type, FOAF["Person"])]
        for uri in uris:
            persons.append(self.get(uri))
        return persons
    
    def get(self, uri):
        uri = [s for s in STORE.subjects(RDF.type, FOAF["Person"])][0]
        name = [o for o in STORE.objects(URIRef(uri), FOAF["nickname"])][0]
        p = self.model(User.objects.all()[0], name)
        return p
        

class Person(models.Model):
    #user = models.ForeignKey(User, unique=True)
    #user = OneToOneField(User)
    name = models.CharField(max_length=100, # default='anonymous',
                           blank=True) # , null=True
    #objects = PersonManager()

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
    #    return self.get_absolute_url()
        return "/person/"
        #return ('person', [])
        #return ('djsmob.views.person')
        #return ('djsmob-person')

    def __unicode__(self):
        #return unicode(self.user.username)
        return self.uri()

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

        #namespaces
        [STORE.bind(*x) for x in NS.items()]
        uri = URIRef(self.uri())
        STORE.add((uri, RDF.type, FOAF["Person"]))
        STORE.add((uri, RDF.type, FOAF['PersonalProfileDocument']))
        STORE.add((uri, FOAF['maker'], uri))
        STORE.add((uri, FOAF['primaryTopic'],uri))
        STORE.add((uri, FOAF['nickname'],Literal(self.name)))
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

User.profile = property(lambda u: Person.objects.get_or_create(user=u)[0])


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
            print instance
            uri = instance[0]
            container = instance[1]
            content = instance[2]
            created = instance[3]
            title = instance[4]
            reply_of = instance[5]
            reply_of_of = instance[6]
            presence = instance[7]
            location = instance[8]
            locname = instance[9]
            post = Post(slug = uri.replace(str(POST_URI),''), 
                        content= content, created=created, 
                        reply_of = reply_of, location = location)
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
            print instance
            #uri, container, content, created, title, reply_of, 
            #reply_of_of, presence, location, locname = instance
            container = instance[0]
            content = instance[1]
            created = instance[2]
            title = instance[3]
            reply_of = instance[4]
            reply_of_of = instance[5]
            presence = instance[6]
            location = instance[7]
            locname = instance[8]
            post = Post(slug = slug, 
                        content= content, created=created, 
                        reply_of = reply_of, location = location)
        return post

class Post(models.Model):
    #uri = models.URLField(_(''), default=''+self.created, editable=False)
    slug = models.SlugField(unique=True, editable=False)
    content = models.CharField(_('content'), max_length=140)
    created = models.DateTimeField(_('sent'), default=datetime.now, editable=False)
    #reply_of = models.URLField(_(''), default='', editable=False)
    reply_of = models.ForeignKey('Post', blank=True, null=True)
    location = models.ForeignKey(Location, blank=True, null=True)
    
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
        #super(Post, self).save(*args, **kwargs)
        print(self.slug)
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
        STORE.add((post_uri, DCT["title"], Literal('Updated - '+self.content)))
        if self.reply_of:
            STORE.add((post_uri, SIOC["reply_of"], URIRef(self.reply_of.uri())))
        
        #opo_uri = URIRef(self.opo_uri())
        #STORE.add((opo_uri, RDF.type, OPO["OnlinePresence"]))
        #STORE.add((opo_uri, OPO["declaredOn"], URIRef(self.has_creator())))
        #STORE.add((opo_uri, OPO["declaredBy"], URIRef(self.maker())))
        #STORE.add((opo_uri, OPO["StartTime"], Literal(self.created)))
        #STORE.add((opo_uri, OPO["customMessage"], post_uri))
        
        if self.location:
            STORE.add((opo_uri, OPO["currentLocation"], URIRef(self.location.uri)))
            STORE.add((URIRef(self.location.uri), RDFS["label"], Literal(self.location.label)))
        #STORE.add(())
        

        rdf=STORE.serialize(format="nt", max_depth=1)
        print rdf
