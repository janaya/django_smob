from django.conf import settings
from rdflib import URIRef

uri = graph = pattern = webid_uri = hub_uri = tag = \
privacy_preference_graph = privacy_preference = post_uri = condition \
= site_uri = triples = person_nick = date = ""

site_uri = URIRef(settings.SITE_URL).n3()
"""
Delete from graph URI

"""
query = """DELETE FROM <%s>""" % uri


"""
Drop URI
"""
query = """DROP <%s>""" % uri


"""
Load URI

"""
query = """LOAD <%s>""" % graph


"""
Load a URI into graph URI

"""
query = """LOAD <%s> INTO <%s>""" % (graph, uri)


"""
Insert triples into graph URI

"""
query = """INSERT INTO <%s> { %s }""" % (graph, triples)


"""
Select all triples from a graph URI

"""
query = """SELECT *
WHERE { 
    GRAPH <%s> {
        ?s ?p ?o
    }
}""" % graph


"""
Ask pattern

"""
query = """ASK %s""" % pattern



"""
Select location from WebID uri

"""
query = """SELECT DISTINCT ?time ?location ?name WHERE {
    GRAPH ?g {
        ?presence opo:currentLocation ?location ;
            opo:StartTime ?time ;
            opo:declaredBy <%s> .
        ?location rdfs:label ?name
        }
    }
ORDER BY DESC(?time)
LIMIT 1"""  % webid_uri

"""
Select name from WebID URI

"""
query = """SELECT ?name WHERE { <%s> foaf:name ?name } LIMIT 1""" % webid_uri


"""
Select predicates, objects from the WebID URI

"""
query = """SELECT DISTINCT ?o WHERE { <%s> ?p ?o } LIMIT 1""" % webid_uri


"""
Select hub URI from hub graph URI

"""
query = """SELECT DISTINCT ?s WHERE { GRAPH <%s> { ?s a smob:Hub } } LIMIT 1""" % hub_uri


"""
Select post uris from tag

"""
query = """SELECT DISTINCT ?uri
WHERE {
    [] sioc:addressed_to ?uri .
    ?uri sioc:name '%s' .
}""" % tag


"""
Select tag uri from tag

"""
query = """SELECT DISTINCT ?uri
WHERE {
    [] tags:associatedTag '%s' ;
        moat:tagMeaning ?uri .
}""" % tag


"""
Select followers from WebID URI

"""
query = """SELECT DISTINCT ?uri
WHERE {?uri sioc:follows <%s>}""" % webid_uri


"""
Select followings from WebID URI

"""
query = """SELECT DISTINCT ?uri
WHERE {<%s> sioc:follows ?uri}""" % webid_uri


"""
Get a WebID URI RSA keys

"""
query = """
  SELECT ?mod ?exp  WHERE {
    [] cert:identity <%s>;
       a rsa:RSAPublicKey;
       rsa:modulus ?mod ;
       rsa:public_exponent ?exp .
  }""" % uri

query = """SELECT ?mod ?exp  WHERE {
    [] a rsa:RSAPublicKey;
        cert:identity <%s>;
        rsa:modulus  [ cert:hex ?mod ] ;
        rsa:public_exponent  [ cert:decimal ?exp ] .
  } """ % uri


"""
Delete RSA keys for a WebID URI

"""
query = """
    DELETE {
      ?sig a rsa:RSAPublicKey .
      ?sig cert:identity <%s> .
                ?sig rsa:modulus ?mod .
                ?sig rsa:public_exponent ?exp .
    }
    WHERE {
      ?sig a rsa:RSAPublicKey;
          cert:identity <%s> ;
                    rsa:modulus ?mod ;
                    rsa:public_exponent ?exp .
    }""" % (uri, uri)

"""
Get relationships from WebID URI

"""
query = """SELECT ?person ?rel_type ?rel_label FROM <%s> WHERE {
  <%s> ?rel_type ?person .
  ?person a foaf:person .
  ?rel_type rdfs:isDefinedBy <http://purl.org/vocab/relationship/> .
  ?rel_type rdfs:label ?rel_label . }""" % (graph, uri)
  # rdfs:subPropertyOf foaf:knows
query = """SELECT ?person ?rel_type ?rel_label FROM <%s> WHERE {
   <%s> ?rel_type ?person .
   FILTER(REGEX(?rel_type, 'http://purl.org/vocab/relationship/', 'i')).
   OPTIONAL { ?rel_type rdfs:label ?rel_label  } 
   }""" % (graph, uri)


"""
Get privacy preference from graph URI

"""
query = """SELECT * FROM <%s> WHERE {
    <%s> a ppo:PrivacyPreference;
        ppo:appliesToResource rdfs:MicroblogPost;
        ppo:hasCondition [
                  ppo:hasProperty moat:taggedWith ;
                  ppo:resourceAsObject ?hashtag .
                  ];
        ppo:assignAccess acl:Read;
        ppo:hasAccessSpace [ ppo:hasAccessQuery ?accessquery ] .
    }""" % (privacy_preference_graph, privacy_preference)

"""
Get privacy preferences

"""
query = """SELECT DISTINCT ?pp ?condition ?accessquery WHERE {
?pp a ppo:PrivacyPreference;
  ppo:appliesToResource rdfs:MicroblogPost;
  ppo:assignAccess acl:Read;
  ppo:hasAccessSpace [ ppo:hasAccessQuery ?accessquery ] ;
  ppo:hasCondition ?condition.
}"""

query = """SELECT DISTINCT ?pp ?hashtag ?accessquery WHERE {
?pp a ppo:PrivacyPreference;
  ppo:appliesToResource rdfs:MicroblogPost;
  ppo:assignAccess acl:Read;
  ppo:hasAccessSpace [ ppo:hasAccessQuery ?accessquery ] ;
ppo:hasCondition [
          ppo:hasProperty moat:taggedWith ;
          ppo:resourceAsObject ?hashtag .
          ].
}"""


"""
Select access spaces from privacy preference post uri

"""
query = """SELECT ?accessquery WHERE {
  ?pp <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vocab.deri.ie/ppo#PrivacyPreference>;
    <http://vocab.deri.ie/ppo#hasCondition> ?x;
    <http://vocab.deri.ie/ppo#hasAccessSpace> ?y.
  ?x <http://vocab.deri.ie/ppo#resourceAsObject> ?hashtag .
  ?y <http://vocab.deri.ie/ppo#hasAccessQuery> ?accessquery .
  <%s> <http://moat-project.org/ns#taggedWith> ?hashtag .
}""" % post_uri

query = """SELECT ?accessquery WHERE {
  ?pp a ppo:PrivacyPreference;
      ppo:hasCondition ?x;
      ppo:hasAccessSpace ?y.
  ?x ppo:resourceAsObject ?hashtag .
  ?y ppo:hasAccessQuery ?accessquery .
  <%s> moat:taggedWith ?hashtag .
}""" % post_uri


"""
Get hashtag from condition

"""
query = """SELECT ?hashtag WHERE {
    '%s' ppo:hasPropery moat:taggedWith.
    OPTIONAL { '%s'  ppo:resourceAsObject ?hashtag }
}""" % (condition, condition)



"""
Get post

"""
query = """SELECT ?p ?v
WHERE {
<%s> rdf:type sioct:MicroblogPost ;
    sioc:content ?content ;
    sioc:has_creator ?creator ;
    foaf:maker ?author ;
    dct:created ?date .
?presence opo:customMessage <%s> .
    OPTIONAL { <%s> sioc:reply_of ?reply_of. }
    OPTIONAL { ?reply_of_of sioc:reply_of <%s> . }
    OPTIONAL { ?author foaf:depiction ?depiction. } 
    OPTIONAL { ?author foaf:img ?depiction . }
    OPTIONAL { ?author foaf:name ?name . }
    OPTIONAL {
        ?presence opo:currentLocation ?location .
        ?location rdfs:label ?locname .
    }
} """ % (uri, uri, uri, uri)


"""
Get post

"""
query = """SELECT DISTINCT ?content ?author ?creator ?date ?presence ?reply_of ?reply_of_of ?depiction ?name ?location ?locname
WHERE {
<%s> rdf:type sioct:MicroblogPost ;
    sioc:content ?content ;
    dct:created ?date ;
    sioc:has_creator ?creator ;
    foaf:maker ?author .
?presence opo:customMessage <%s> .
    OPTIONAL { <%s> sioc:reply_of ?reply_of. }
    OPTIONAL { ?reply_of_of sioc:reply_of <%s> . }
    OPTIONAL { ?author foaf:depiction ?depiction. } 
    OPTIONAL { ?author foaf:img ?depiction . }
    OPTIONAL { ?author foaf:name ?name . }
    OPTIONAL {
        ?presence opo:currentLocation ?location .
        ?location rdfs:label ?locname .
    }
} """ % (uri, uri, uri, uri)

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
} """ % post_uri

"""
Get posts

"""
query = """SELECT DISTINCT ?post_uri ?content ?author ?creator ?created ?title 
?presence ?reply_of ?reply_of_of ?depiction ?name ?location ?locname
WHERE {
    ?post_uri rdf:type sioct:MicroblogPost ;
    sioc:has_container %s;
    sioc:content ?content ;
    sioc:has_creator ?creator ;
    foaf:maker ?author ;
    dct:created ?created ;
    dct:title ?title.
?presence opo:customMessage ?post_uri ;
    opo:declaredOn ?creator;
    opo:declaredBy ?maker;
    opo:StartTime ?created.
    OPTIONAL { ?post_uri sioc:reply_of ?reply_of. }
    OPTIONAL { ?reply_of_of sioc:reply_of ?post_uri . }
    OPTIONAL { ?author foaf:depiction ?depiction. } 
    OPTIONAL { ?author foaf:img ?depiction . }
    OPTIONAL { ?author foaf:name ?name . }
    OPTIONAL {
        ?presence opo:currentLocation ?location .
        ?location rdfs:label ?locname .
    }
} """ % site_uri


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
} """ % site_uri

query_posts = """SELECT DISTINCT ?post_uri ?container ?content ?created     ?title ?reply_of ?reply_of_of ?presence ?location ?locname    WHERE {        ?post_uri rdf:type sioct:MicroblogPost ;    sioc:has_container %s;    sioc:content ?content ;    dct:created ?created ;    dct:title ?title.    OPTIONAL { ?post_uri sioc:reply_of ?reply_of. }    OPTIONAL { ?reply_of_of sioc:reply_of ?post_uri . }    OPTIONAL {        ?presence opo:currentLocation ?location .        ?location rdfs:label ?locname .    }} """ % site_uri

#select = ("?post_uri", "?container", "?content", "?created", "?title", 
#"?reply_of", "?reply_of_of", "?presence", "?location", "?locname")
#where = GraphPattern([
#            ("?post_uri", RDF["type"], SIOCT["MicroblogPost"]),
#            ])

"""
Get posts URI from WebID URI

"""
query = """
SELECT DISTINCT ?post
WHERE {
    ?post rdf:type sioct:MicroblogPost ;
        foaf:maker <%s>;
} 
""" % webid_uri


"""
Get post from person nick

"""
query = """SELECT DISTINCT ?person ?user WHERE {
  ?post rdf:type sioct:MicroblogPost .
  ?post sioc:has_creator ?user .
  ?post foaf:maker ?person .
  ?person foaf:nick '%s' .
}""" % person_nick


"""
Get post location

"""
query = """SELECT ?lat ?long 
WHERE { <%s> geo:lat ?lat ; geo:long ?long .}""" % post_uri


"""
Select posts older than x days 

"""
query = """SELECT DISTINCT ?graph
WHERE {
    GRAPH ?graph {
        ?post a sioct:MicroblogPost ;
            dct:created ?date ;
            foaf:maker ?author .
        FILTER (?date < '%s') .
        FILTER (?author != <%s>) .
    } 
    OPTIONAL { ?post rev:rating ?star }
    FILTER (!bound(?star))
}""" % (date, webid_uri)


"""
Get users from post

"""
query = """SELECT ?user ?name
WHERE {
    <%s> sioc:addressed_to ?user .
    ?user sioc:name ?name .
}""" % post_uri


"""
Get tags from post

"""
query = """SELECT ?tag ?uri
WHERE {
    ?tagging a tags:RestrictedTagging ;
        tags:taggedResource <%s> ;
        tags:associatedTag ?tag ;
        moat:tagMeaning ?uri .
}""" % post_uri
