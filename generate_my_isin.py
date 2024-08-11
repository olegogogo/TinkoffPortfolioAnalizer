from tinkoff.invest import Client
import pandas as pd

MY_TOKEN = "t.LRfvexBeY1eCsgBhZL2XbAWo7_zCjgzTBcbdWa_u4d-WBQMlflGUthl9h1yIdPVdrXlHV-H9smLQjojrgWsCyg"
BROKER_COMMISSION = 0.003


def to_df(response):
    accounts = response.accounts

    data = []
    for account in accounts:
        data.append({
            'id': account.id,
            'type': account.type.name,
            'name': account.name,
            'status': account.status.name,
            'opened_date': account.opened_date,
            'closed_date': account.closed_date,
            'access_level': account.access_level.name
        })
    data = pd.DataFrame(data)
    data.drop(['closed_date', 'access_level'], inplace=True, axis=1)
    return data


def convert_quantity(quotation):
    if type(quotation) == dict:
        return quotation['units'] + quotation['nano'] / 1e9
    else:
        return quotation.units + quotation.nano / 1e9


with Client(MY_TOKEN) as client:
    response = client.users.get_accounts()
    accounts = to_df(response)
    portfolio = client.operations.get_portfolio(account_id=str(accounts[accounts['name'] == 'Bonds']['id'].tolist()[0]))
    all_bonds = pd.DataFrame(client.instruments.bonds().instruments)

bonds_account_id = accounts[accounts['name'] == 'Bonds']['id'].tolist()[0]

bonds_data = pd.DataFrame([])
for i, position in enumerate(portfolio.positions):
    bonds_data.loc[i, 'figi'] = position.figi

my_isin = pd.merge(bonds_data, all_bonds[['figi', 'isin']], on='figi', how='inner')
my_isin['isin'].to_excel('my_bonds.xlsx', index=False, header=False)
