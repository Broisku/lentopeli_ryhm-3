from functions.get_airport_type import get_airport_type
from functions.buy_terminal import buy_terminal
from inputThread import player_input_queue


def view_terminal(connect, player, icao):
    cursor = connect.cursor(buffered=True)
    airport_typ = get_airport_type(connect, icao)
    print("Available terminal type for your airport:")
    if airport_typ == "small_airport":
        type = "small"
    elif airport_typ == "medium_airport":
        type = "medium"
    else:
        type = "large"

    cursor.execute(
        "select size, cost, construction_time, operating_cost, yield from terminal_types where size = %s", (type,))
    stats = cursor.fetchall()
    print(stats)
    print("HOW TO READ: (size, cost, construction time, operating cost, yield)")

    cursor.execute("""
                    select type from airport join player_airports
                    on airport.player_airports_id = player_airports.id join game
                   on player_airports.game_id = game.id
                   where game.name = %s and gps_code = %s""", (player, icao,))
    result_airport_type = cursor.fetchone()
    airport_type = result_airport_type[0]

    cursor.execute("""select terminal_types.id 
                    from terminal_types
                      join player_terminal
                            on player_terminal.terminal_types_id = terminal_types.id
                        join player_airports pa1
                             on player_terminal.player_airports_id = pa1.id
                        join game
                            on pa1.game_id = game.id
                        join player_airports pa2
                             on player_terminal.player_airports_id = pa2.id
                        join airport
                            on airport.player_airports_id = pa2.id
                        where game.name = %s 
                         and gps_code = %s""", (player, icao,))

    result_terminal_count = cursor.fetchall()

    if airport_type == "small_airport":
        if len(result_terminal_count) < 1:
            print("Terminals available for small airport: 1 small terminal")
        else:
            print("No terminals available")
            return
        print("cost for terminal: 3,000,000")

    if airport_type == "medium_airport":
        if len(result_terminal_count) < 1:
            print("Terminals available for medium airport: 2 medium terminals")
        elif len(result_terminal_count) < 2:
            print("Terminals available for medium airport: 1 medium terminal")
        else:
            print("No terminals available")
            return
        print("cost for terminal: 6,000,000")

    if airport_type == "large_airport":
        if len(result_terminal_count) < 1:
            print("Terminals available for large airport: 3 large terminals")
        elif len(result_terminal_count) < 2:
            print("Terminals available for large airport: 2 large terminals")
        elif len(result_terminal_count) < 3:
            print("Terminals available for large airport: 1 large terminal")
        else:
            print("No terminals available")
            return
        print("cost for terminal: 12,000,000")

    print("type buy to buy terminal or type exit ")
    player_action = player_input_queue.get()
    if player_action == "buy":
        buy_terminal(connect, player, icao)
    elif player_action == "exit":
        cursor.close()
        return

    cursor.close()