import polars as pl
import requests
import time
import os

def fetch_cid_from_pubchem(smiles):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/cids/TXT"
    try:
        response = requests.get(url)
        response.raise_for_status()
        cid = response.text.strip()
        if cid == "0":
            return "no_data"  # Return 'no_data' if the CID is 0
        elif cid:  # Check if the CID is not empty
            return cid
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching CID for SMILES '{smiles}': {e}")
        return None

def process_smiles(input_parquet, output_parquet):
    # Load the input DataFrame
    df_input = pl.read_parquet(input_parquet).rename({'SMILES_mongo':'smiles'})
    df_input = df_input.unique(subset="smiles")
    
    # Check if the output file exists and load processed data
    if os.path.exists(output_parquet):
        df_output = pl.read_parquet(output_parquet)
        processed_smiles = set(df_output['smiles'].to_list())
    else:
        df_output = pl.DataFrame({"smiles": [], "cid": []})
        processed_smiles = set()
    
    # Filter out SMILES that have already been processed
    df_to_process = df_input.filter(~pl.col("smiles").is_in(processed_smiles))
    
    # Process each SMILES and save after every 100 iterations
    new_rows = []
    iteration_count = 0
    for smiles in df_to_process["smiles"].to_list():
        cid = fetch_cid_from_pubchem(smiles)

        print(smiles, cid)
        
        if cid:  # Only add to the output if CID is not None
            new_rows.append({"smiles": smiles, "cid": cid})
        else:
            print(f"SMILES '{smiles}' could not be found on PubChem or returned an empty CID.")
        
        iteration_count += 1
        
        # Save the DataFrame to disk every 100 iterations
        if iteration_count % 100 == 0:
            if new_rows:
                new_df = pl.DataFrame(new_rows)
                df_output = pl.concat([df_output, new_df])
                df_output.write_parquet(output_parquet)
                print(f"Saved output DataFrame to '{output_parquet}' after {iteration_count} iterations.")
                new_rows = []  # Clear the list after saving

        time.sleep(1)  # To avoid hitting PubChem API rate limits
    
    # Save any remaining rows after finishing processing
    if new_rows:
        new_df = pl.DataFrame(new_rows)
        df_output = pl.concat([df_output, new_df])
        df_output.write_parquet(output_parquet)
        print(f"Final save of output DataFrame to '{output_parquet}'.")

if __name__ == "__main__":
    input_parquet = "../data/MINES/mongo_predicted_compounds.parquet"
    output_parquet = "../data/MINES/pubchem_output_smiles_cid.parquet"
    
    while True:
        try:
            process_smiles(input_parquet, output_parquet)
            print("Processing completed successfully.")
            break
        except Exception as e:
            print(f"Script crashed with error: {e}. Restarting...")
            time.sleep(5)  # Wait for 5 seconds before restarting
