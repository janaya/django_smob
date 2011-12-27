from rdflib import Namespace, URIRef
from django.conf import settings

# common namespaces

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


RSS10 = Namespace("http://purl.org/rss/1.0/" )
CC = Namespace("http://web.resource.org/cc/")
RSS10_CONTENT = Namespace("http://purl.org/rss/1.0/modules/content/")
ADMIN = Namespace("http://webns.net/mvcb/")
ATOM = Namespace("http://www.w3.org/2005/Atom")


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

# site specific namespaces
# FIXME: change settings by config?
SITE_URI = URIRef(settings.SITE_URL)
HUB_URI = URIRef(settings.SITE_URL + "/data/hub")
RSS_URI = URIRef(settings.SITE_URL + "/rssrdf/post/")
FOAF_DOC_URI = URIRef(settings.SITE_URL + "/data/person")
FOAF_URI = URIRef(settings.SITE_URL + "/data/person#id")
POST_URI = Namespace(settings.SITE_URL + "/data/post/")
FOLLOWINGS_URI = URIRef(settings.SITE_URL + "/data/followings")
FOLLOWERS_URI = URIRef(settings.SITE_URL + "/data/followers")
PRIVACY_PREFERENCES_URI = URIRef(settings.SITE_URL + "/data/privacy_preferences")
PRIVACY_PREFERENCE_URI = URIRef(settings.SITE_URL + "data/privacy_preference/")
OPO_URI = URIRef(settings.SITE_URL + "/data/person#presence")
