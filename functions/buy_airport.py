from functions.fetch_airport_cost import get_airport_cost
from functions.check_availability import check_availability

def buy_airport(icao, connect, player):
    #tarkistetaan ensin onko lentokenttä saatavilla
    if check_availability(connect, icao):
        print("Airport is not available for purchase")
        return

    cursor = connect.cursor(buffered=True)
    cursor.execute("select money from game where name = %s", (player,))
    result = cursor.fetchone()

    money = result[0]

    airport_cost = get_airport_cost(icao, connect)

    if money >= airport_cost:
        cursor.execute("update game set money = money - %s where name = %s", (airport_cost, player,))
        add_airport = "insert into player_airports(yield) values(0)"
        cursor.execute(add_airport)
        player_airport_id = cursor.lastrowid
        cursor.execute("update airport set player_airports_id = %s where gps_code = %s", (player_airport_id, icao,))
        cursor.execute("update game set player_airports_id = %s where name = %s", (player_airport_id, player,))
        print(f"{icao} airport purchased succesfully")
    else:
        print("You do not have enough money")
    cursor.close()