import polars as pl
import defl as defl
from tqdm import tqdm

import matplotlib.pyplot as plt
import statistics
from pymongo import MongoClient

df = pl.read_parquet("../data/MINES/reactions_compounds_list.parquet")

# Filter out rows with empty lists
df_filtered = df.filter((pl.col("starting_compounds").list.len() > 0) & (pl.col("predicted_compounds").list.len() > 0))

# Ensure both columns have matching element counts
df = df_filtered.explode(['starting_compounds']).explode(['predicted_compounds'])

predicted_elements_list = df["starting_compounds"].unique().to_list()


# Define the fields to retrieve
taxonomy_fields = [
    "organism_taxonomy_01domain",
    "organism_taxonomy_02kingdom",
    "organism_taxonomy_03phylum",
    "organism_taxonomy_04class",
    "organism_taxonomy_05order",
    "organism_taxonomy_06family",
    "organism_taxonomy_07tribe",
    "organism_taxonomy_08genus",
    "organism_taxonomy_09species",
    "organism_taxonomy_10varietas"
]


# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string

# Select the database
db = client['lotus_mines_enzymatic']

# Select the collection
collection = db['lotus']


for taxom in taxonomy_fields:
    result_list = list()
    
    for starting_compound_id in predicted_elements_list:
        # Query to find the document by _id and retrieve only the taxonomy fields
        result = collection.find(
            {"_id": starting_compound_id}, 
            {
                taxom: 1,
                "_id": 1
            }
        )

        for one_result in result:
            result_list.append(one_result)
        
        
    df_taxonomy = pl.DataFrame(result_list, infer_schema_length=10000)
    
    
    df_joined = df.join(df_taxonomy, left_on="starting_compounds", right_on="_id", how="left", coalesce=True)
    df_joined.write_parquet("../data/taxom_"+taxom+".parquet")

    print(f"done with {taxom}")
