from django.conf import settings

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

"""
Get post without webid

"""

"""
    OPTIONAL { ?post_uri sioc:reply_of ?reply_of. }
    OPTIONAL { ?reply_of_of sioc:reply_of ?post_uri . }
    OPTIONAL {
        ?presence opo:currentLocation ?location .
        ?location rdfs:label ?locname .
    }
"""
query_post_rdf = """
CONSTRUCT {
    %s rdf:type sioct:MicroblogPost ;
    sioc:content ?content ;
    dct:created ?created ;
    dct:title ?title.
}
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
} """ # % (uri, uri)

"""
Insert triples into graph URI

"""
query_insert_into_graph_triples = """INSERT INTO <%s> { %s }""" 
#% (graph, triples)

"""
Select all triples from a graph URI

"""
query_select_graph = """SELECT *
WHERE { 
    GRAPH <%s> {
        ?s ?p ?o
    }
}""" #% graph

"""
Get graph

"""

query_construct_graph = """ CONSTRUCT { ?s ?p ?o } 
WHERE { GRAPH %s { ?s ?p ?o } . }""" # % graph


query_construct_graph_filter_date = """CONSTRUCT { ?s ?p ?o } WHERE
 {
   GRAPH ?g { ?s ?p ?o } .
   { ?g dct:created ?date } .
   FILTER ( dct:created(?date) > "2005-02-28T00:00:00Z"^^xsd:dateTime ) .
 }"""
