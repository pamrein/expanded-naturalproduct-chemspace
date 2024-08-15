# module defl = dataset extractor for Lotus


import polars as pl
import numpy as np
import os, sys

# change the configsetting, to see the full tables
pl.Config.set_tbl_rows(100)
pl.Config(fmt_str_lengths=550)

# Example of loading LOTUS datasets with polars (python module)
def load_lotus_csv(path_file):
    df_lotus = pl.read_csv(
            path_file,
            infer_schema_length=50000,
            null_values=["", "NA"],
            schema_overrides=
            {
                "structure_xlogp": pl.Float32,
                "structure_cid": pl.UInt32,
                "organism_taxonomy_ncbiid": pl.UInt32,
                "organism_taxonomy_ottid": pl.UInt32,
                "structure_stereocenters_total": pl.UInt32,
                "structure_stereocenters_unspecified": pl.UInt32,
            },
        )
    
    df_lotus = df_lotus.with_columns(
            pl.col("organism_taxonomy_gbifid")
            .map_elements(lambda x: np.nan if x.startswith("c(") else x)
            .cast(pl.UInt32)
            .alias("organism_taxonomy_gbifid")
        )
    return df_lotus


def find_predicted_compounds(df: pl.dataframe, SMILES_INPUT: str) -> pl.LazyFrame:
    # Step 1: Find all the entries with the specific SMILES id
    df_SMILES = df.filter(pl.col("id") == SMILES_INPUT)

    # Step 2: Filter for the starting compounds
    df_new = df_SMILES.filter(pl.col("type") == "Starting Compound")

    # Step 3: Get all the unique reaction_id
    df_reactions = df_new.select("reaction_id").unique()

    # Step 4: Filter the original DataFrame to include only the rows with the desired reaction_id and type == "Predicted"
    df_result = df.filter(
        pl.col("reaction_id").is_in(df_reactions) & 
        (pl.col("type") == "Predicted")
    )
   
    return df_result