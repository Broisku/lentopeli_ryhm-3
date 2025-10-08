from functions.get_airport_type import get_airport_type
from functions.get_bank_balance import give_bank_balance
from functions.get_airport_id import get_airport_id


def buy_runway(connect, player, icao):
    balance = give_bank_balance(connect, player)
    airport_type = get_airport_type(connect, icao)
    if airport_type == "small_airport":
        runway_id = 0
        runway_cost = 3_000_000
        if balance < runway_cost:
            print("You don't have enough money!")
            return
    elif airport_type == "medium_airport":
        runway_id = 1
        runway_cost = 6_000_000
        if balance < runway_cost:
            print("You don't have enough money!")
            return
    else:
        runway_id = 2
        runway_cost = 9_000_000
        if balance < runway_cost:
            print("You don't have enough money!")
            return
    airport_id = get_airport_id(connect, player, icao)
    cursor = connect.cursor()
    cursor.execute("""
    insert into player_runway (player_airports_id, runway_types_id) values (%s, %s)
                   """, (airport_id, runway_id))
    cursor.execute("update game set money = money - %s where name = %s", (runway_cost, player,))
    print("Runway purchase successful!")
    cursor.close()