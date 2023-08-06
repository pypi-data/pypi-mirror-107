import json
import requests
import pandas
from pandas.io.json import json_normalize
import urllib3

#url host to be update with api.unicarbkb.org
__host_url = "https://flaskapp-cr-v1-gateway-v3vtg36c3q-ue.a.run.app/"
urllib3.disable_warnings()
#__selected_version = API_VERSION.V1

def set_host_url(url):
    global __host_url
    __host_url = url


def search_glytoucan(glytoucan):
    """
    Search database for metadata associated with the queried glytoucan accession
    Returns: glytoucan, wurcs, inchi, smiles_isomeric, glycam, iupac, mass, mass_pme
    """
    url = "{host}/get-glytoucan-structure-details/{glytoucan}".format(host=__host_url, glytoucan=glytoucan)
    result = requests.get(url)

    if result.status_code == 200:
        return result
    else:
        # raise the error
        result.raise_for_status()

def get_proteoglycoforms(uniprot):
    """
    Search database for metadata associated with queried uniprot accession
    Returns: uniprot, glytoucan, position, pmid
    """
    url = "{host}/get-proteoglycoforms/{uniprot}".format(host=__host_url, uniprot=uniprot)
    result = requests.get(url)
    #print(result.)

    if result.status_code == 200:
        return result
    else:
        # raise the error
        result.raise_for_status()

def get_glycan_structure_gts(glytoucan):
    """
    Search database for metadata associated with queried uniprot accession
    Returns: uniprot, protein, taxonomy
    """
    url = "{host}/get-glycan-structure-gts/{glytoucan}".format(host=__host_url, glytoucan=glytoucan)
    result = requests.get(url)
    #print(result.text)

    if result.status_code == 200:
        return result
    else:
        # raise the error
        result.raise_for_status()


def get_glytoucan_published_glycoforms(uniprot):
    """
    Search database for metadata associated with queried uniprot accession
    Returns: uniprot, glytoucan, position, pmid
    """
    url = "{host}/get-glytoucan-published-glycoforms/{uniprot}".format(host=__host_url, uniprot=uniprot)
    result = requests.get(url)
    #print(result.text)

    if result.status_code == 200:
        return result
    else:
        # raise the error
        result.raise_for_status()

def get_glytoucan_structure_details(uniprot):
    """
    Search database for metadata associated with queried uniprot accession
    Returns: glytoucan, wurcs, inchi, smiles , glycam, iupac, mass, mass_pme
    """
    url = "{host}/get-glytoucan-structure-details/{uniprot}".format(host=__host_url, uniprot=uniprot)
    result = requests.get(url)
    #print(result.text)

    if result.status_code == 200:
        return result
    else:
        # raise the error
        result.raise_for_status()

def get_sequence_formats(glytoucan):
    """
    Get sequence formats for specified glytoucan accession
    """
    url = "{host}/get-sequence-formats/{glytoucan}".format(host=__host_url, glytoucan=glytoucan)
    result = requests.get(url)
    #print(result.text)

    if result.status_code == 200:
        return result
    else:
        # raise the error
        result.raise_for_status()

def search_sequence_format_wurcs(wurcs):
    """
    Search database for structure matching WURCS string
    """
    url = "{host}/search-sequence-format-wurcs/{wurcs}".format(host=__host_url, wurcs=wurcs)
    result = requests.get(url)
    #print(result.text)

    if result.status_code == 200:
        return result
    else:
        # raise the error
        result.raise_for_status()

def search_mass(mass):
    """
    Search by mass
    """
    url = "{host}/search-mass/{mass}".format(host=__host_url, mass=mass)
    result = requests.get(url)
    #print(result.text)

    if result.status_code == 200:
        return result
    else:
        # raise the error
        result.raise_for_status()

def search_mass_glycoprotein(mass):
    """
    Search mass and return glycoproteins
    """
    url = "{host}/search-mass-glycoprotein/{mass}".format(host=__host_url, mass=mass)    
    result = requests.get(url)

    if result.status_code == 200:
        return result
    else:
        #raise the error
        result.raise_for_status()

def search_composition(composition):
    """
    Search composition
    Multiple params search, see swagger docs
    """
    print("COMPOSITION: " + composition)
    url = "{host}/search-composition?{composition}".format(host=__host_url, composition=composition)
    result = requests.get(url)
    #print(result.text)

    if result.status_code == 200:
        return result
    else:
        # raise the error
        result.raise_for_status()







