import matplotlib.pyplot as plt
from matplotlib_venn import venn3

# Counts
counts = {
    'Kegg': 4198,
    'Brenda': 5656,
    'Metacyc': 5258,
    'Kegg and Brenda': 3250,
    'Kegg and Metacyc': 3783,
    'Brenda and Metacyc': 3756,
    'Brenda and Metacyc and Kegg': 3002
}

# Calculate the sizes of each set
sizes = {
    '100': counts['Brenda'] - counts['Kegg and Brenda'] - counts['Brenda and Metacyc'] - counts['Brenda and Metacyc and Kegg'],
    '010': counts['Kegg'] - counts['Kegg and Brenda'] - counts['Kegg and Metacyc'] - counts['Brenda and Metacyc and Kegg'],
    '001': counts['Metacyc'] - counts['Kegg and Metacyc'] - counts['Brenda and Metacyc'] - counts['Brenda and Metacyc and Kegg'],
    '110': counts['Kegg and Brenda'] - counts['Brenda and Metacyc and Kegg'],
    '101': counts['Kegg and Metacyc'] - counts['Brenda and Metacyc and Kegg'],
    '011': counts['Brenda and Metacyc'] - counts['Brenda and Metacyc and Kegg'],
    '111': counts['Brenda and Metacyc and Kegg']
}

# Plot Venn diagram
venn = venn3(subsets=(sizes['100'], sizes['010'], sizes['110'], sizes['001'], sizes['101'], sizes['011'], sizes['111']),
             set_labels=('Brenda', 'Kegg', 'Metacyc'))

# Display the diagram
plt.title("Venn Diagram of Dataset Overlaps")
plt.savefig("/home/popeye/2024_GitHub_Master_Bioinformatics/additional_scripts/dataset_venn_diagram.png")

