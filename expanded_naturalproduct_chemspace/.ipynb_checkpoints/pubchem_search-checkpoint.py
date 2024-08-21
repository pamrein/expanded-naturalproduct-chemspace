import requests
from bs4 import BeautifulSoup
import pymongo
import polars as pl
from tqdm import tqdm
from pymongo import MongoClient
import defl as defl
import urllib.parse


def check_smiles_in_pubchem(smiles):
    # URL encode the SMILES string
    smiles_encoded = urllib.parse.quote(smiles)
    
    # Use the PubChem API to convert SMILES to a CID (PubChem Compound ID)
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles_encoded}/cids/JSON"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'IdentifierList' in data and 'CID' in data['IdentifierList']:
            cids = data['IdentifierList']['CID']
            if cids:
                cid = cids[0]
                #print(f"SMILES found in PubChem with CID: {cid}")
                return cid
            else:
                print("SMILES not found in PubChem.")
                return None
        else:
            print("Unexpected response format.")
            return None
    else:
        #print(f"Error in accessing PubChem API. Status code: {response.status_code}")
        return None

def get_organisms_for_cid(cid):
    # Use the PubChem API to retrieve organisms associated with the CID
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON/?heading=Taxonomy"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        organisms = []
        if 'Record' in data and 'Section' in data['Record']:
            for section in data['Record']['Section']:
                if section.get("TOCHeading") == "Taxonomy":
                    for subsection in section.get("Section", []):
                        if subsection.get("TOCHeading") == "Organisms":
                            for info in subsection.get("Information", []):
                                organisms.append(info.get("Name", "Unknown organism"))
        return organisms
    else:
        #print(f"Error in retrieving organism data. Status code: {response.status_code}")
        return []


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

=======
"""
>>>>>>> c7e1eb7 (update all)
=======
"""
>>>>>>> c7e1eb7 (update all)
=======
"""
>>>>>>> c7e1eb7 (update all)
=======
"""
>>>>>>> c7e1eb7 (update all)
# connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['compounds']

result = client['lotus_mines_enzymatic']['compounds'].find()

documents_list = list(result)

df_mongo = pl.DataFrame(documents_list)
df_mongo = df_mongo.drop(["Generation", "Expand", "Reactant_in", "Product_of", "Type"])
df_mongo = df_mongo.rename({"_id":"_id_mongo", 
                            "ID":"ID_mongo", 
                            "SMILES":"SMILES_mongo", 
                            "InChI_key":"InChI_key_mongo"})
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
"""

df_mongo = pl.read_parquet("../data/MINES/mongo_predicted_compounds.parquet")
>>>>>>> c7e1eb7 (update all)
=======
"""

df_mongo = pl.read_parquet("../data/MINES/mongo_predicted_compounds.parquet")
>>>>>>> c7e1eb7 (update all)
=======
"""

df_mongo = pl.read_parquet("../data/MINES/mongo_predicted_compounds.parquet")
>>>>>>> c7e1eb7 (update all)
=======
"""

df_mongo = pl.read_parquet("../data/MINES/mongo_predicted_compounds.parquet")
>>>>>>> c7e1eb7 (update all)

# compare SMILES_mongo or smiles_lotus
smiles_list = df_mongo["SMILES_mongo"].unique().to_list()
smiles_list = smiles_list
cid_list = list()

print(f'df shape: {df_mongo.shape}  | SMILES list: {len(smiles_list)}')


# Iterate over the DataFrame rows and update CID
for smiles in smiles_list:
    cid = check_smiles_in_pubchem(smiles)

    if cid == None:
        cid_list.append(None)
    else:
        cid_list.append(cid)

# Print the updated DataFrame
print(f'cid_list [{len(cid_list)}], smiles_list [{len(smiles_list)}]')

# Create a new DataFrame with SMILES and CID
df_smiles_cid = pl.DataFrame({
    "SMILES_mongo": smiles_list,
    "CID": cid_list
})


df_joined = df_starting.join(df_smiles_cid, on="SMILES_mongo", how="left")
df_joined.write_parquet("../data/MINES/pubchem_all_compounds.parquet")