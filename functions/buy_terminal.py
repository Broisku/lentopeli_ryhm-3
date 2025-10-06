from functions.get_airport_type import get_airport_type
from functions.get_bank_balance import give_bank_balance
from functions.get_airport_id import get_airport_id

def buy_terminal(connect, player, icao):
    balance = give_bank_balance(connect, player)
    airport_type = get_airport_type(connect, icao)
    if airport_type == "small_airport":
        terminal_id = 0
        terminal_cost = 3_000_000
        if balance < terminal_cost:
            print("You don't have enough money!")
            return
    elif airport_type == "medium_airport":
        terminal_id = 1
        terminal_cost = 6_000_000
        if balance < terminal_cost:
            print("You don't have enough money!")
            return
    elif airport_type == "large_airport":
        terminal_id = 2
        terminal_cost = 12_000_000
        if balance < terminal_cost:
            print("You don't have enough money!")
            return
    airport_id = get_airport_id(connect, player, icao)
    cursor = connect.cursor()
    cursor.execute("""
                   insert into player_terminal (player_airports_id, terminal_types_id)
                   values (%s, %s)
                   """, (airport_id, terminal_id))
    cursor.execute("update game set money = money - %s where name = %s", (terminal_cost, player,))
    print("Terminal purchase successful!")
    cursor.close()