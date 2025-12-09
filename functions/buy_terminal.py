from functions.get_airport_type import get_airport_type
from functions.get_bank_balance import give_bank_balance
from functions.get_airport_id import get_airport_id

def buy_terminal(connect, player, icao):
    balance = give_bank_balance(connect, player)
    airport_type = get_airport_type(connect, icao)

    if airport_type == "small_airport":
        terminal_id = 0
    elif airport_type == "medium_airport":
        terminal_id = 1
    else:
        terminal_id = 2

    cursor = connect.cursor(dictionary=True)
    cursor.execute("select size, cost, construction_time, operating_cost, yield from terminal_types where id=%s",
                   (terminal_id,))
    terminal = cursor.fetchone() #terminaalin tiedot sanakirjana, sarakkeen nimet ovat sanakirjan avaimia

    if balance < terminal["cost"]:
        print("You don't have enough money!")
        return "You don't have enough money!"
    airport_id = get_airport_id(connect, player, icao)
    cursor.execute("""
                   insert into player_terminal (player_airports_id, terminal_types_id, construction_weeks_left)
                   values (%s, %s, %s)
                   """, (airport_id, terminal_id, terminal["construction_time"]))
    cursor.execute("update game set money = money - %s where name = %s", (terminal["cost"], player,))
    print("Terminal purchase successful!")
    connect.commit()
    cursor.close()
    return "Terminal purchase successful!"
