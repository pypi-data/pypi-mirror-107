'''
unicarbkb_glygen_api: Test module.

Meant for use with py.test.
Write each test as a function named test_<something>.
Read more here: http://pytest.org/

Copyright 2021, Matthew Campbell
Licensed under MIT
'''
from unicarbkb_glygen_api import app as api
import unittest
import json, urllib.parse


class UnicarbkbGlygenApiTest(unittest.TestCase):
    maxDiff = None


    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    # setup
    def setUp(self):
        super().setUp()
        api.set_host_url("https://flaskapp-cr-v1-gateway-v3vtg36c3q-ue.a.run.app")
        #url host to be update with api.unicarbkb.org
        
    # test search
    def test_search(self):
        """
        Test that we get a wurcs string and mass for specified glytoucan accession
        """
        print("test_search_glytoucan")
        glytoucan="G43638QT"
        search_results = api.search_glytoucan(glytoucan)
        search_results_json = search_results.json()

        data = search_results_json[0]["f0_"] #f0_ default for bigquery to_string output query

        jtopy=json.dumps(data) 
        dict_json=json.loads(jtopy)
     
        payload = json.loads(dict_json)

        wurcs_output = payload["wurcs"]
        mass_output = payload["mass"]

        self.assertTrue(wurcs_output != "")
        self.assertTrue(mass_output > 0.0)

    def test_structure_gts(self):
        """
        Test that we get a list of gts for a given glytoucan id
        """
        print("test_structure_gts")
        glytoucan="G17689DH"
        search_results = api.get_glycan_structure_gts(glytoucan)
        search_results_json = search_results.json()
        #print(search_results_json)
        data = search_results_json[0]["f0_"] #f0_ default for bigquery to_string output query
        jtopy=json.dumps(data) 
        dict_json=json.loads(jtopy)
     
        payload = json.loads(dict_json)

        uniprot_output = payload["uniprot"]
        protein_output = payload["protein"]

        self.assertTrue(protein_output != "")


    def test_glycoform(self):
        """
        Test that we get a list of glycoforms for the specified uniprot accession
        """
        print("test_glycoforms")
        uniprot="P14210-1"
        search_results = api.get_proteoglycoforms(uniprot)
        search_results_json = search_results.json()
        #print(search_results_json)
        data = search_results_json[0]["f0_"] #f0_ default for bigquery to_string output query
        jtopy=json.dumps(data) 
        dict_json=json.loads(jtopy)
     
        payload = json.loads(dict_json)

        uniprot_output = payload["uniprot"]
        glytoucan_output = payload["glytoucan"]

        self.assertTrue(uniprot_output != "")
        self.assertTrue(glytoucan_output != "")

    def test_glytoucan_published_glycoforms(self):
        """
        Test that we get a list of glycoforms for the specified uniprot accession
        """
        print("test_published_glycoforms")
        uniprot="P14210-1"
        search_results = api.get_glytoucan_published_glycoforms(uniprot)
        search_results_json = search_results.json()
        #print(search_results_json)
        data = search_results_json[0]["f0_"] #f0_ default for bigquery to_string output query
        jtopy=json.dumps(data) 
        dict_json=json.loads(jtopy)
     
        payload = json.loads(dict_json)

        glytoucan_output = payload["uniprot"]
        self.assertTrue(glytoucan_output != "")

    def test_glytoucan_structure_details(self):
        """
        Test that we get a list of glycoforms for the specified uniprot accession
        """
        print("test_glytoucan_structure_details")
        uniprot="P14210-1"
        search_results = api.get_glytoucan_published_glycoforms(uniprot)
        search_results_json = search_results.json()
        #print(search_results_json)
        data = search_results_json[0]["f0_"] #f0_ default for bigquery to_string output query
        jtopy=json.dumps(data) 
        dict_json=json.loads(jtopy)
     
        payload = json.loads(dict_json)

        uniprot_output = payload["uniprot"]
        self.assertTrue(uniprot_output != "")

    def test_sequence_formats(self):
        """
        Test that we get sequences for search glytoucan accession
        """
        print("test_sequence_formats")
        glytoucan="G17689DH"
        search_results = api.get_sequence_formats(glytoucan)
        search_results_json = search_results.json()
        data = search_results_json[0]["f0_"] #f0_ default for bigquery to_string output query
        jtopy=json.dumps(data) 
        dict_json=json.loads(jtopy)
     
        payload = json.loads(dict_json)

        wurcs_output = payload["wurcs"]
        self.assertTrue(wurcs_output != "")

    #def test_search_sequence_format_wurcs(self):
    #    """
    #    Test that WURCS string can be found
    #    """
    #    print("test_sequence_format_wurcs")
    #    wurcs="WURCS=2.0/2,2,1/[h4334h][a4334h-1x_1-4]/1-2/a?-b1"
    #    search_results = api.search_sequence_format_wurcs( urllib.parse.quote(wurcs, safe='') )
    #    search_results_json = search_results.json()
    #    data = search_results_json[0]["f0_"] #f0_ default for bigquery to_string output query
    #    jtopy=json.dumps(data) 
    #    dict_json=json.loads(jtopy)
     
    #    payload = json.loads(dict_json)

     #   wurcs_output = payload["wurcs"]
     #   self.assertTrue(wurcs_output != "")

    def test_search_mass(self):
        """
        Test searching by mass
        """
        print("test_mass_search")
        mass="180"
        search_results = api.search_mass(mass)
        search_results_json = search_results.json()
        data = search_results_json[0]["f0_"] #f0_ default for bigquery to_string output query
        jtopy=json.dumps(data) 
        dict_json=json.loads(jtopy)
     
        payload = json.loads(dict_json)

        mass_output = payload["mass"]
        self.assertTrue(mass_output != "")

    def test_search_mass_glycoprotein(self):
        """
        Test searching by mass
        This will get associated glycoproteins
        """ 
        print("test_mass_search_glycoprotein")
        mass="180"
        search_results = api.search_mass_glycoprotein(mass)
        search_results_json = search_results.json()
        data = search_results_json[0]["f0_"] #f0_ default for bigquery to_string output query
        jtopy=json.dumps(data) 
        dict_json=json.loads(jtopy)
     
        payload = json.loads(dict_json)

        mass_output = payload["mass"]
        self.assertTrue(mass_output != "")

    def test_search_composition(self):
        """
        Test searching by composition
        """
        #print("test_composition_search")
        composition = "hex=3&hexnac=4"
        search_results = api.search_composition(composition)
        search_results_json = search_results.json()
        #print(search_results_json)
        data = search_results_json[0]["f0_"] 
        jtopy=json.dumps(data) 
        dict_json=json.loads(jtopy)
     
        payload = json.loads(dict_json)

        glytoucan_output = payload["glytoucan_ac"]
        self.assertTrue(glytoucan_output != "")

    


if __name__ == '__main__':
    unittest.main()



