# objective: transfer PD PSM table to DART-ID input
from sys import argv
import pandas as pd

script, fin = argv

# read table and separate to two (byonic and sequest) by search engine
df = pd.read_excel(fin)

df_byonic = df.loc[df["Identifying Node"].str.contains("PMI")]
df_sequest = df.loc[df["Identifying Node"].str.contains("Seq")]

# print("df.shape", df.shape)
# print("df_byonic.shape", df_byonic.shape)
# print("df_sequest.shape", df_sequest.shape)

# filter and output to final table
df_byonic = df_byonic.sort_values(['PEP 2D'],ascending=False)
df_sequest = df_sequest.sort_values(['Percolator PEP'],ascending=False)

# print(df_byonic[:5][["RT [min]",'|Log Prob|', 'Byonic Score', 'Delta Byonic Score', 'Delta Mod Score',
#        'PEP 2D', 'q-Value 2D', 'FDR 2D', 'Peptide Group FDR 2D', 'PEP 1D',
#        'q-Value 1D', 'FDR 1D', 'Peptide Group FDR 1D']])

# print(df_sequest[:1].columns)


df_sequest = df_sequest.rename(index=str,columns={
    # required columns
    "Annotated Sequence": 'Modified sequence',
    "Percolator PEP":"PEP",
    "RT [min]": "Retention time",
    "Spectrum File": "Raw file",
    # optional columns below
    "Protein Accessions": "Proteins",
    "Master Protein Accessions": "Leading razor protein"})

df_sequest["Retention length"] = "0.1"

# output
df_sequest.to_csv(fin+"sequest.csv", sep="\t")


df_byonic = df_byonic.rename(index=str,columns={
    # required columns
    "Annotated Sequence": 'Modified sequence',
    "PEP 2D":"PEP",
    "RT [min]": "Retention time",
    "Spectrum File": "Raw file",
    # optional columns below
    "Protein Accessions": "Proteins",
    "Master Protein Accessions": "Leading razor protein",
})
df_byonic["Retention length"] = "0.1"


# output
df_byonic.to_csv(fin+"byonic.csv", sep="\t")
