from functions.fetch_airport_cost import get_airport_cost
from functions.check_availability import check_availability

def buy_airport(icao, connect, player):
    #tarkistetaan ensin onko lentokenttä saatavilla
    if not check_availability(connect, icao, player):
        print("You already own this airport!")
        return

    cursor = connect.cursor(buffered=True)
    cursor.execute("select money from game where name = %s", (player,))
    result = cursor.fetchone()

    money = result[0]

    airport_cost = get_airport_cost(icao, connect)

    if money >= airport_cost:

        # päivitetään pelaajan raha
        cursor.execute("update game set money = money - %s where name = %s", (airport_cost, player,))

        cursor.execute("insert into player_airports(yield, game_id) select 0, game.id from game where name = %s", (player,))

        player_airport_id = cursor.lastrowid
        cursor.execute("update airport set player_airports_id = %s where gps_code = %s", (player_airport_id, icao,))

        print(f"{icao} airport purchased succesfully!")

    else:
        print("You don't have enough money for this airport!")

    connect.commit()
    cursor.close()