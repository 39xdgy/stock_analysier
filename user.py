from webull import paper_webull, webull

class user:

    def __init__(self, user_login_info, stock_list):
        self.stock_list = stock_list
        self._login_info = user_login_info
        self.wb = webull()#paper_webull()


    def get_login_info(self):
        return self._login_info

    def login(self):
        self.wb.login(self._login_info['email'], self._login_info['psw'], self._login_info["name"], "994897", self._login_info["questionID"], self._login_info["questionAns"])
        print("Success")


if __name__ == "__main__":
    import json
    f = open("webull.json",)
    json_user = json.load(f)
    print(json_user)
    test_user = user(json_user, [])
    test_user.login()
    test_user.wb.refresh_login()
    #test_user.wb.get_trade_token("741037")
    print(test_user.wb.get_detail())
    #print(test_user.wb.get_trade_token(json_user['token']))
    #print(test_user.wb.get_mfa('39xdgy@gmail.com'))
    print(test_user.wb.get_security('+1-3192102312'))
    test_user.wb.place_order(stock = "AAPL", action = "BUY", price = 140, orderType = "LMT", quant = 1)