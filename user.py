from webull import paper_webull, webull
import json
class user:

    def __init__(self):
        #self.stock_list = stock_list
        #self._login_info = user_login_info
        self.wb = webull()#paper_webull()
        self.pwb = paper_webull()

    '''
    def get_login_info(self):
        return self._login_info
    '''

    def login_trading(self, json_path):
        fh = open(json_path, 'r')
        credential_data = json.load(fh)
        fh.close()

        self.wb._refresh_token = credential_data['refreshToken']
        self.wb._access_token = credential_data['accessToken']
        self.wb._token_expire = credential_data['tokenExpireTime']
        self.wb._uuid = credential_data['uuid']

        n_data = self.wb.refresh_login()

        credential_data['refreshToken'] = n_data['refreshToken']
        credential_data['accessToken'] = n_data['accessToken']
        credential_data['tokenExpireTime'] = n_data['tokenExpireTime']

        file = open('webull_credentials.json', 'w')
        json.dump(credential_data, file)
        file.close()

        # important to get the account_id
        return self.wb.get_account_id()

    def login_paper_trading(self, json_path):
        fh = open(json_path, 'r')
        credential_data = json.load(fh)
        fh.close()

        self.pwb._refresh_token = credential_data['refreshToken']
        self.pwb._access_token = credential_data['accessToken']
        self.pwb._token_expire = credential_data['tokenExpireTime']
        self.pwb._uuid = credential_data['uuid']

        n_data = self.pwb.refresh_login()

        credential_data['refreshToken'] = n_data['refreshToken']
        credential_data['accessToken'] = n_data['accessToken']
        credential_data['tokenExpireTime'] = n_data['tokenExpireTime']

        file = open('webull_credentials.json', 'w')
        json.dump(credential_data, file)
        file.close()

        # important to get the account_id
        return self.pwb.get_account_id()


if __name__ == "__main__":
    test_user = user()
    wb_id = test_user.login_trading("webull_credentials.json")
    pwb_id = test_user.login_paper_trading("webull_credentials.json")
    print(wb_id)
    print(pwb_id)