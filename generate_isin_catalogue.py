from tinkoff.invest import Client
import pandas as pd
from generate_my_isin import MY_TOKEN

with Client(MY_TOKEN) as client:
    all_bonds = pd.DataFrame(client.instruments.bonds().instruments)

all_bonds = all_bonds[all_bonds['buy_available_flag'] == True]

all_bonds['isin'].to_excel('all_bonds.xlsx', index=False, header=False)
