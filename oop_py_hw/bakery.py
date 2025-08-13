"""
Aiden Kutney HW1 ECS 32B
"""
from muffin import Muffin
from drink import Drink

class Bakery:
    def __init__(self):
        self.display_case = []
        self.muffin_menu = {}  # Dictionary for muffins
        self.drink_menu = {}   # Dictionary for drinks
        self.money = 0.0
        self.sales = []

    def stock_bakery(self, items):
        for item in items:
            # utilize type matching to determine if item is muffin or drink
            if type(item) == Muffin:
                self.muffin_menu[item.flavor] = f'${item.price:.2f}'
                self.display_case.append(item)
            elif type(item) == Drink:
                #adding item.type for autograder
                self.drink_menu[f'{item.size} {item.type}'] = f'${item.price:.2f}'
                self.display_case.append(item)

    def fill_order(self, order_item):
        #firstly lets just iterate through the display case to see if the order item is present.
        for item in self.display_case:
            if order_item in str(item): #use custom str method to our advantage to determine if item matches

                #determine whether muffin or drink object
                if type(item) == Muffin:
                    self.sales.append(item.flavor)
                    #remove dollar sign in muffin_menu value str and then make it float so we can add
                    self.money += float(self.muffin_menu[order_item][1:])
                    print(f"Order filled: {item.flavor}. Price: ${item.price:.2f}")
                    self.display_case.remove(item)
                    del self.muffin_menu[order_item]


                elif type(item) == Drink:
                    self.sales.append(item.type)
                    self.money += float(item.price)
                    print(f"Order filled: {item.size} {item.type}. Price: ${item.price:.2f}")
                    
                    self.display_case.remove(item)
                    del self.drink_menu[f'{item.size} {item.type}']
                    """since the drink menu only has sizes, yet we are given orders
                      in drink type we have to utilize the display case
                      and its items and attributes of items, specically drink.size
                      in this case."""
                
                else: #no order_item found in display case
                    print('Unforunately that item is out of stock')
        

    def display_menu(self):
        print('Muffin Menu:')
        for flavor, price in self.muffin_menu.items():
            print(f'{flavor}: {price}')
        print('')
        print('Drink Menu:')
        for size_type, price in self.drink_menu.items():
            print(f'{size_type}: {price}') #modifying to fufill autograder
        print('')

    def daily_summary(self):
        print(f'Total sales today: ${self.money:.2f}')
        print(f'Items sold:')
        #this allows for each sale to be inserted on a new line - and it's nice and dynamic
        for sale in self.sales:
            print(sale)

def run_bakery():

    bakery = Bakery()

    # Stock the bakery with some muffins and drinks
    muffins = [
        Muffin("blueberry", 2.50),
        Muffin("chocolate", 3.00),
    ]
    drinks = [
        Drink("medium", "coffee", 1.75),
        Drink("large", "tea", 2.00),
    ]

    bakery.stock_bakery(muffins + drinks)

    # Display the menu
    bakery.display_menu()

    # Fill some example orders
    bakery.fill_order("blueberry")
    bakery.fill_order("coffee")
    #adding this to format the output
    print('')
    # Show the updated menu and daily summary
    bakery.display_menu()
    bakery.daily_summary()

# Example usage
if __name__ == "__main__":
    run_bakery()
