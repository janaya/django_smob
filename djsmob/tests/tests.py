from django.test import TestCase
from djsmo.models import *

class DjangoSMOBTestCase(TestCase):
    def setUp(self):
        #fixtures = ['person.json', 'person']
        self.configuration = Configuration(
            external_webid_uri = 'http://xmppwebid.github.com/xmppwebid/julia')
        self.hub = Hub()
        self.person = Person(name = 'duy')
        self.interest = Interest(label = 'Semantic Web', 
                            uri = 'http://dbpedia.org/resource/Semantic_Web')
        self.relationship = Relationship(rel_uri = '',
            rel_label='knows', to_person_uri = 'http://apassant.net')

    def test_hub(self):
        self.assertEqual(self.hub.rdf(), "<http://localhost:8000> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://vocab.deri.ie/push/SemanticHub>")

    def test_configuration(self):
        pass

    def test_person(self):
        pass

    def test_interest(self):
        pass
    
    def test_relationship(self):
        pass
        
    def test_edit_person(self):
        response = self.client.get('/person/edit')
        self.assertEqual(response.status_code, 200)
        self.assertEqual([poll.pk for poll in resp.context['latest_poll_list']], [1])
        
##def suite():
##    tests = ['testHub', 'testPerson']
##
##    return unittest.TestSuite(map(DjangoSMOBTestCase, tests))
##
##suite = unittest.TestLoader().loadTestsFromTestCase(WidgetTestCase)
