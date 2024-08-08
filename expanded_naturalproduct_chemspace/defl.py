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