from Attribute import attribute_dict

class Trigger():
    self.attribute      = None
    self.value          = None
    self.bias           = None

    def __init__(self, attribute, value, bias):
        # 'attribute' will be a string; match it with the
        # correct instance using attribute_dict
        self.attribute  = attribute_dict[attribute]
        self.value      = value
        self.bias       = bias
        return True

    def __str__(self):
        return '{1} {2} {3}'.format(attribute, value, bias)
