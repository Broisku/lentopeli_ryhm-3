def check_availability(connect, icao):
    cursor = connect.cursor()
    cursor.execute("select player_airports_id from airport where ident=%s", (icao,))
    result = cursor.fetchone()
    cursor.close()
    return result[0]