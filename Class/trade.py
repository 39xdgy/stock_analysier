class trade:

    def __init__(self, name = "", start_time = "", end_time = "", start_price = -1, end_price = -1, amount = 0, earning = 0):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.start_price = start_price
        self.end_price = end_price
        self.amount = amount
        self.earning = earning

    def __str__(self):
        output_str = f'Stock name: {self.name}\n'
        output_str += f'\tStart time: {self.start_time} \tEnd time: {self.end_time}\n'
        output_str += f'\tStart price: {self.start_price} \tEnd price: {self.end_price}\n'
        output_str += f'\tEarning: {self.earning} \tAmount: {self.amount}'

        return output_str

    def get_data(self):
        return {
            'name': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'start_price': self.start_price,
            'end_price': self.end_price,
            'amount': self.amount,
            'earning': self.earning
        }

    def buy_update(self, name, start_time, start_price, amount):
        self.name = name
        self.start_time = start_time
        self.start_price = start_price
        self.amount = amount
    
    def sell_update(self, end_time, end_price):
        self.end_time = end_time
        self.end_price = end_price
        self.earning = (self.start_price - self.end_price) * self.amount
