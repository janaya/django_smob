from django.conf import settings
#from rdflib import URIRef

#site_uri = URIRef(settings.SITE_URL).n3()


"""
Get posts without webid

"""
query_posts = """SELECT DISTINCT ?post_uri ?container ?content ?created 
?title ?reply_of ?reply_of_of ?presence ?location ?locname
WHERE {
    ?post_uri rdf:type sioct:MicroblogPost ;
    sioc:has_container %s;
    sioc:content ?content ;
    dct:created ?created ;
    dct:title ?title.
    OPTIONAL { ?post_uri sioc:reply_of ?reply_of. }
    OPTIONAL { ?reply_of_of sioc:reply_of ?post_uri . }
    OPTIONAL {
        ?presence opo:currentLocation ?location .
        ?location rdfs:label ?locname .
    }
} """ 

"""
Get post without webid

"""
query_post = """SELECT ?container ?content ?created ?title 
?reply_of ?reply_of_of ?presence ?location ?locname
WHERE {
    %s rdf:type sioct:MicroblogPost ;
    sioc:content ?content ;
    dct:created ?created ;
    dct:title ?title.
    OPTIONAL { ?post_uri sioc:reply_of ?reply_of. }
    OPTIONAL { ?reply_of_of sioc:reply_of ?post_uri . }
    OPTIONAL {
        ?presence opo:currentLocation ?location .
        ?location rdfs:label ?locname .
    }
} """
