def get_airport_id(connect, player, icao):
    cursor = connect.cursor()
    cursor.execute("""
    select player_airports.id
    from player_airports, game, airport
                   where player_airports.game_id = game.id
                   and airport.player_airports_id = player_airports.id
                   and game.name = %s
                   and gps_code = %s
                   """,(player, icao))
    airport_id = cursor.fetchone()
    airport_id = airport_id[0]
    cursor.close()
    return airport_id