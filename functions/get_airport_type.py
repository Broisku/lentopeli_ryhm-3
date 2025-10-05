def get_airport_type(connect, icao):
    cursor = connect.cursor()
    cursor.execute("select type from airport where gps_code = %s", (icao,))
    airport_type = cursor.fetchone()[0]
    cursor.close()
    return airport_type