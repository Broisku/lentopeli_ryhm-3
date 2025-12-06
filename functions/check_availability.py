def check_availability(connect, icao, player):
    cursor = connect.cursor()
    cursor.execute("""
                   select airport.player_airports_id 
                   from airport 
                            join player_airports 
                                 on airport.player_airports_id = player_airports.id 
                            join game 
                                 on player_airports.game_id = game.id 
                   where gps_code=%s and game.name = %s
                   """,(icao, player,))
    result = cursor.fetchone()
    cursor.close()
    if result is None:
        return True
    else:
        return False