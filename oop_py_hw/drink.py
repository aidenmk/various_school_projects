class Drink:
    def __init__(self, size, type, price):
        self.size = size
        self.type = type
        self.price = price

    def __str__(self):
        return f"""A {self.size}, {self.type} drink costing {self.price}"""