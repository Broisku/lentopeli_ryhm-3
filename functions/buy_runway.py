from functions.get_airport_type import get_airport_type
from functions.get_bank_balance import give_bank_balance
from functions.get_airport_id import get_airport_id


def buy_runway(connect, player, icao):
    balance = give_bank_balance(connect, player)
    airport_type = get_airport_type(connect, icao)

    if airport_type == "small_airport":
        runway_id = 0
    elif airport_type == "medium_airport":
        runway_id = 1
    else:
        runway_id = 2

    cursor = connect.cursor(dictionary=True)
    cursor.execute("select length, cost, construction_time, operating_cost, yield from runway_types where id=%s",
                   (runway_id,))
    runway = cursor.fetchone()  # kiitoradan tiedot sanakirjana, sarakkeiden nimet ovat sanakirjan avaimia

    if balance < runway["cost"]:
        print("You don't have enough money!")
        return

    airport_id = get_airport_id(connect, player, icao)
    cursor = connect.cursor()
    cursor.execute("""
    insert into player_runway (player_airports_id, runway_types_id) values (%s, %s)
                   """, (airport_id, runway_id))
    # Päivitetään player_airports.yield
    sum_yield = runway["yield"] - runway["operating_cost"]
    cursor.execute("UPDATE player_airports SET yield = yield + %s WHERE id = %s", (sum_yield, airport_id))
    cursor.execute("update game set money = money - %s where name = %s", (runway["cost"], player,))
    print("Runway purchase successful!")
    cursor.close()