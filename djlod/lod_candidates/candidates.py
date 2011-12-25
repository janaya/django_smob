import urllib2
from xml.dom.minidom import parse, parseString
import json

DBPEDIA_BASE_URL = "http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?QueryString=%s&QueryClass=&MaxHits=10"
SINDICE_BASE_URL = "http://api.sindice.com/v2/search?page=1&q=%s&qt=term&format=json"
GEO_BASE_URL = "http://ws.geonames.org/searchJSON?q=%s&maxRows=10"
GEO_BASE_URI = "http://sws.geonames.org/"
term = "RDF"

def get_dbpedia_candidates(term):
    candidates = {}
    
    url = DBPEDIA_BASE_URL % term
    f = urllib2.urlopen(url)
    xml = f.read()

    dom = parseString(xml)
    results = dom.getElementsByTagName("Result")
    for r in results:
        label_nodes = r.getElementsByTagName("Label")[0]
        label = label_nodes.childNodes[0].nodeValue
        uri_nodes = r.getElementsByTagName("URI")[0]
        uri = uri_nodes.childNodes[0].nodeValue
        candidates[label]=uri
    return candidates


def get_sindice_candidates(term):
    candidates = {}
    
    url = SINDICE_BASE_URL % term
    f = urllib2.urlopen(url)
    json_string = f.read()
    
    json_data = json.loads(json_string)
    for entry in json_data['entries']:
        candidates[entry['title'][0]] = entry['link']
    return candidates


def get_geo_candidates(term):
    candidates = {}
    
    url = GEO_BASE_URL % term
    f = urllib2.urlopen(url)
    json_string = f.read()
    
    json_data = json.loads(json_string)
    for geoname in json_data['geonames']:
        uri = GEO_BASE_URI + str(geoname['geonameId']) + "/"
        label = geoname['name'] + "(" + geoname['countryName'] + ")"
        candidates[label] = uri
    return candidates
