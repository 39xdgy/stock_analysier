import json
from webull import paper_webull, webull # for real trading, import 'webull'

wb = webull()


fh = open('../Data/webull_credentials.json', 'r')
credential_data = json.load(fh)
fh.close()

wb._refresh_token = credential_data['refreshToken']
wb._access_token = credential_data['accessToken']
wb._token_expire = credential_data['tokenExpireTime']
wb._uuid = credential_data['uuid']

n_data = wb.refresh_login()
credential_data['refreshToken'] = n_data['refreshToken']
credential_data['accessToken'] = n_data['accessToken']
credential_data['tokenExpireTime'] = n_data['tokenExpireTime']

file = open('../Data/webull_credentials.json', 'w')
json.dump(credential_data, file)
file.close()

# important to get the account_id
#print(wb.get_account_id())
#print(wb.get_detail())
account_info = wb.get_account()
'''
for key in account_info:
    print(f'{key}: {account_info[key]}')
'''

radio = 2 / 3
base = 5000

outcome = float(account_info['netLiquidation']) * radio // base * base
print(outcome)
#print(wb.place_order(stock = "AAPL", action = "BUY", orderType = "MKT", enforce = "DAY", quant = 2))