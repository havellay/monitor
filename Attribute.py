class Attribute():
    name    = ''

    def get_name(self):
        return self.name

    def calculate(self, symbol):
        # base class knows nothing about calculate
        return None

class RSI(Attribute):
    self.name   = 'RSI'

    def calculate_RSI(Symbol):
        return None

    def __str__(self):
        return self.name

    def calculate(self, symbol):
        pass

# attribute_list has the names of defined attributes
attribute_dict = {
        'RSI': RSI,
    }
