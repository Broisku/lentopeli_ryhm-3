def get_airport_cost(icao, connect):
    cursor = None
    try:
        cursor = connect.cursor(buffered=True)
        cursor.execute("select type from airport where gps_code = %s", (icao,))
        result = cursor.fetchone()
        if result is None:
            raise ValueError(f"{icao} is not a valid ICAO code")

        airport_type = result[0]

        if airport_type == "small_airport":
            airport_cost = 3_000_000
        elif airport_type == "medium_airport":
            airport_cost = 8_000_000
        else:
            airport_cost = 15_000_000
        return airport_cost
    finally:
        if cursor:
            cursor.close()