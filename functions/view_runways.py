from functions.get_airport_type import get_airport_type
from functions.buy_runway import buy_runway


def view_runway(connect, player, icao):
    cursor = connect.cursor(buffered=True)
    airport_typ = get_airport_type(connect, icao)
    print("Available runway type for your airport:")
    if airport_typ == "small_airport":
        cursor.execute("select length, cost, construction_time, operating_cost, yield from runway_types where length = 1500")
        small_stats = cursor.fetchall()
        print(small_stats)
    elif airport_typ == "medium_airport":
        cursor.execute("select length, cost, construction_time, operating_cost, yield from runway_types where length = 3000")
        medium_stats = cursor.fetchall()
        print(medium_stats)
    else:
        cursor.execute("select length, cost, construction_time, operating_cost, yield from runway_types where length = 4500")
        large_stats = cursor.fetchall()
        print(large_stats)

    print("HOW TO READ: (length in meters, cost, construction time, operating cost, yield")
    cursor.execute("""
                    select type from airport join player_airports
                    on airport.player_airports_id = player_airports.id join game
                   on game.player_airports_id = player_airports.id
                   where game.name = %s and gps_code = %s""", (player, icao,))
    result_airport_type = cursor.fetchone()
    airport_type = result_airport_type[0]

    cursor.execute("""select runway_types.id 
                    from runway_types
                      join player_runway
                            on player_runway.runway_types_id = runway_types.id
                        join player_airports pa1
                             on player_runway.player_airports_id = pa1.id
                        join game
                            on game.player_airports_id = pa1.id
                        join player_airports pa2
                             on player_runway.player_airports_id = pa2.id
                        join airport
                            on airport.player_airports_id = pa2.id
                      where game.name = %s 
                        and gps_code = %s
                        """, (player, icao,))

    result_runway_count = cursor.fetchall()
    if airport_type == "small_airport":
        if len(result_runway_count) < 1:
            print("Runways available for small airport: 2 x 1500m runway")
        elif len(result_runway_count) < 2:
            print("Runways available: 1 x 1500m runway")
        else: print("No runways available")
        print("cost for runway: 3,000,000")
        player_action = input("type buy to buy runway or type exit")
        if player_action == "buy":
            buy_runway(connect, player, icao)
        elif player_action == "exit":
            return

    if airport_type == "medium_airport":
        if len(result_runway_count) < 1:
            print("Runways available for medium airport: 3 x 3000m runways")
        elif len(result_runway_count) < 2:
            print("Runways available: 2 x 3000m runway")
        elif len(result_runway_count) < 3:
            print("Runways available: 1 x 3000m runway")
        else: print("No runways available")
        print("cost for runway: 6,000,000")
        player_action = input("type buy to buy runway or type exit")
        if player_action == "buy":
            buy_runway(connect, player, icao)
        elif player_action == "exit":
            cursor.close()
            return

    if airport_type == "large_airport":
        if len(result_runway_count) < 1:
            print("Runways available for large airport: 4 x 4500m runways")
        elif len(result_runway_count) < 2:
            print("Runways available: 3 x 4500m runway")
        elif len(result_runway_count) < 3:
            print("Runways available: 2 x 4500m runway")
        elif len(result_runway_count) < 4:
            print("Runways available: 1 x 4500m runway")
        else: print("No runways available")
        print("cost for runway: 9,000,000")
        player_action = input("type buy to buy runway or type exit")
        if player_action == "buy":
            buy_runway(connect, player, icao)
        elif player_action == "exit":
            cursor.close()
            return
    cursor.close()