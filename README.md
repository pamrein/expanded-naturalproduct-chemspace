# expanded-naturalproduct-chemspace
Fork from: <https://github.com/commons-research/expanded-naturalproduct-chemspace>  
[Abstract](/data/abstract.pdf)  
[Masterthesis](/data/expanded_np_chemspace.pdf)

This thesis was carried out at UniFr in the COMMONS Lab <https://www.unifr.ch/bio/en/groups/allard/>.
For six months, I immersed myself in chemical structure expansion using Pickaxe.
In this repository, I have collected all the important scripts from this journey.

All scripts relevant to the MSc thesis ‘Expanded natural product chemspace’ can be found here.  

## scripts
More details about the scripts can be found in the jupyter-lab files.  
(expanded-naturalproduct-chemspace/*)  


[LOTUS overview](/expanded_naturalproduct_chemspace/01_LOTUS_overview.ipynb):  
Small statistics about the used dataset.  

To address the formatting issues in dataset v10, you can read the data with some additional options or preprocessing steps. Here's an example code block:  
```python
import pandas as pd

# Specify the path to the dataset
file_path = "path_to_dataset_v10.csv"

# Read the data with careful handling of formatting issues
data = pd.read_csv(
    file_path,
    delimiter=",",  # Adjust delimiter if necessary
    skipinitialspace=True,  # Remove extra spaces
    error_bad_lines=False,  # Skip problematic lines
    engine="python"  # Use Python engine for flexibility
)

# Display a preview of the dataset
print(data.head())
```

[MINES Input](/expanded_naturalproduct_chemspace/02_MINES_input_files.ipynb):  
Analyzing the Inputdata from Lotus and reaction rules.

[MINES lists](/expanded_naturalproduct_chemspace/03_MINES_reactions.ipynb):  
Script for getting columns of interest. Specifically reactions.

[MINES validation](/expanded_naturalproduct_chemspace/04_MINES_validation.ipynb):  
scripts for validate SMILES in PubChem. (Didn't work with a big dataset)

[MINES taxonomy search](/expanded_naturalproduct_chemspace/05_LOTUS_MINES_taxonomy_search.ipynb):  
Lot of different scripts. Annotating the LOTUS db with the output from pickaxe.

[Plots](/expanded_naturalproduct_chemspace/06_general_plots_for_thesis.ipynb):  
Creating the plots for the master thesis can be found here.
