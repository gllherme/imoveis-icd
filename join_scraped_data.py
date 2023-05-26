import glob
import pandas as pd
import os
from pathlib import Path

path = '/home/guilherme/grad/projetoCienciaDeDados/data_to_join'

all_files = glob.glob(os.path.join(path, "*.csv"))

df_from_each_file = (pd.read_csv(f, encoding='utf-8', sep=';', dtype=str) for f in all_files)
concatenated_df = pd.concat(df_from_each_file, ignore_index=True)

concatenated_df['listing.pricingInfo.salePrice'] = ''

concatenated_df.to_csv('./new_scraped_dataZAP.csv', sep=";", index=False)

