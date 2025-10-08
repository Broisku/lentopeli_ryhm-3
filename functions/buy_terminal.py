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
    elif airport_type == "large_airport":
        terminal_id = 2

    cursor = connect.cursor(dictionary=True)
    cursor.execute("select size, cost, construction_time, operating_cost, yield from terminal_types where id=%s",
                   (terminal_id,))
    terminal = cursor.fetchone() #terminaalin tiedot sanakirjana, sarakkeen nimet ovat sanakirjan avaimia

    if balance < terminal["cost"]:
        print("You don't have enough money!")
        return
    airport_id = get_airport_id(connect, player, icao)
    cursor.execute("""
                   insert into player_terminal (player_airports_id, terminal_types_id)
                   values (%s, %s)
                   """, (airport_id, terminal_id))
    #Päivitetään player_airports.yield
    sum_yield = terminal["yield"]- terminal["operating_cost"]
    cursor.execute("UPDATE player_airports SET yield = yield + %s WHERE id = %s", (sum_yield, airport_id))
    cursor.execute("update game set money = money - %s where name = %s", (terminal["cost"], player,))
    print("Terminal purchase successful!")
    cursor.close()
