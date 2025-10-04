import mysql.connector

connect = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='flight_game',
         user='flight_game_user',
         password='1234',
         autocommit=True
         )

country_iso = input('Enter country iso code')

#show list of possible airports to user

def show_airports():
    sql = f"""
    select type, airport.name, municipality, gps_code, iata_code, elevation_ft, latitude_deg, longitude_deg
    from airport inner join country
    on airport.iso_country = country.iso_country
    where country.iso_country = %s
    order by type desc
    """
    cursor = connect.cursor()
    cursor.execute(sql, (country_iso,))
    airports = cursor.fetchall()

    if airports:
        print(f"\nAirports in {country_iso}: (HOW TO READ: airport size, name, municipality, icao code, iata code, elevation in feet, latitude, longitude) PRICES FOR AIRPORTS: small: 3,000,000; medium: 6,000,000; large: 12,000,000")
        for airport in airports:
            print(airport)

    else:
        print(f"No airports found for {country_iso}")

    cursor.close()

show_airports()
