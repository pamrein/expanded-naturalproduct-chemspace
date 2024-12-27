import polars as pl
import defl as defl
import matplotlib.pyplot as plt
import statistics

df = pl.read_parquet("../data/MINES/reactions_compounds_type_reactant_list.parquet")

df_starting_compounds = df.filter(pl.col("type") == "Starting Compound")
df_starting_compounds = df_starting_compounds.select(pl.col("id")).unique()

predicted_elements = list()
predicted_compound_names = list()

for starting_compound in df_starting_compounds.iter_rows():

    starting_compound_name = starting_compound[0]
    
    df_predicted = defl.find_predicted_compounds(df, starting_compound_name)

    amount_of_predicted_compounds = df_predicted.shape[0]

    predicted_compound_names.append(starting_compound_name)
    predicted_elements.append(amount_of_predicted_compounds)

    # Print detailed progress
    #print(f"{starting_compound_name} found {amount_of_predicted_compounds} compounds")


# Create a Polars DataFrame
df = pl.DataFrame({
    "starting_compound_id": predicted_compound_names,
    "predicted_elements": predicted_elements,
})

df.write_parquet("../data/starting2predicted.parquet")
