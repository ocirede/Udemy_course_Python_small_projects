from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

coffe_maker = CoffeeMaker()
money_machine = MoneyMachine()
menu = Menu()


is_on = True
while is_on:
    options = menu.get_items()
    drink = input(f"What would you like? {options} ")
    if drink == "off":
        is_on = False
    elif drink == "report":
        print(coffe_maker.report())
        print(money_machine.report())
    else:
        chosen_drink = menu.find_drink(drink)
        cost = chosen_drink.cost
        enough_resources = coffe_maker.is_resource_sufficient(chosen_drink)
        if not enough_resources:
            is_on = False
        else:
            payment = money_machine.make_payment(cost)
            if payment:
                coffe_maker.make_coffee(chosen_drink)