class Attribute():
    self.name   = ''

    def get_name():
        return self.name

class RSI(Attribute):
    self.name   = 'RSI'

    def calculate_RSI(Symbol):
        return None

    def __str__(self):
        return self.name

# attribute_list has the names of defined attributes
attribute_dict = {
        'RSI': RSI,
    }
