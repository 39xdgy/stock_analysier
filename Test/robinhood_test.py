from robin_stocks import robinhood as rh

import json, pyotp

user_data = {}
with open('../Data/rh_login.json', 'r') as f:
    user_data = json.load(f)

#print(user_data)

totp = pyotp.TOTP(user_data['token']).now()
print(totp)



#login = rh.login(user_data['user'], user_data['pwd'], mfa_code=totp)

print(rh.build_user_profile())
