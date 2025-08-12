class Muffin():
    def __init__(self, flavor, price):
        self.flavor = flavor
        self.price = price
        self.cook_levels = ['underdone', 'well done', 'overdone']
        self.current_level = 0
    
    def bake_muffin(self):
        if self.current_level < 2:
            self.current_level += 1
    
    def get_description(self):
        # For cooking level, I dynamically use the value from current_level as the index
        description = f"""{self.cook_levels[self.current_level]} {self.flavor} muffin priced at ${self.price:.2f}"""
        return description

    def __str__(self):
        return f"""{self.cook_levels[self.current_level]} {self.flavor} muffin priced at ${self.price:.2f}"""