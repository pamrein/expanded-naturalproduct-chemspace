import polars as pl
import defl as defl
from tqdm import tqdm

import matplotlib.pyplot as plt
import statistics
from pymongo import MongoClient

df = pl.read_parquet("../data/MINES/reactions_compounds_list_ID.parquet")

# Assuming df is your Polars DataFrame and 'starting_compounds_ID' is the column to filter
pattern = r'^\w{14}-\w{11}-\w{1}$'
filtered_df = df.filter(pl.col('starting_compounds_ID').str.contains(pattern))

predicted_elements_list = df["starting_compounds_ID"].unique().to_list()


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


df_lotus = pl.read_parquet("../data/LOTUS/230106_frozen_metadata_cleaned.parquet")

for taxom in taxonomy_fields:
    # Create an empty DataFrame with two string columns
    df_taxonomy = pl.DataFrame({
        "structure_inchikey": pl.Series([], dtype=pl.Utf8),
        taxom: pl.Series([], dtype=pl.Utf8)
    })    

    for starting_compound_ID in predicted_elements_list:
        result = df_lotus.filter(pl.col("structure_inchikey") == starting_compound_ID)
        result = result.select(pl.col(["structure_inchikey", taxom]))

        print(result)
        df_taxonomy = pl.concat([df_taxonomy, result], how="vertical")  


    print(df[1:5])
    print(df_taxonomy[1:5])
    
    df_joined = df.join(df_taxonomy, left_on="starting_compounds_ID", right_on="structure_inchikey", how="left", coalesce=True)
    print(df_joined[0:10])
    df_joined.write_parquet("../data/MINES/taxom_"+taxom+".parquet")

    print(f"done with {taxom}")
