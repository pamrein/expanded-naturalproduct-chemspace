import pubchempy as pcp
import csv, os
import polars as pl

df_mongo = pl.read_parquet("../data/MINES/mongo_predicted_compounds.parquet")
file = "../data/taxonomy/smiles_cid.tsv"
smiles = df_mongo["SMILES_mongo"].unique().to_list()


# Header to add
header = ['smile', 'cid_compound']

# Check if the file exists
if not os.path.exists(file):
    # File does not exist, create it and add the header
    with open(file, 'w', newline='') as file:
        writer = csv.writer(file, delimiter='\t')
        writer.writerow(header)
else:
    print(f"The file '{file}' already exists.")
    

for smile in smiles:
    c = pcp.get_compounds(smile, 'smiles')

    for compound in c:
        cid_compound = compound.cid
                    
        print(cid_compound)
        
        if cid_compound == None:
            print("nothing found")
        else:
            additional_data = [
                [smile, cid_compound],
            ]
            
            # Write data to a TSV file
            with open(filename, 'a', newline='') as file:
                writer = csv.writer(file, delimiter='\t')
                writer.writerows(additional_data)