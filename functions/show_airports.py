def show_airports(connect):
    sql = f"""
    select type, airport.name, municipality, gps_code, iata_code, elevation_ft, latitude_deg, longitude_deg
    from airport inner join country
    on airport.iso_country = country.iso_country
    where country.iso_country = %s
    order by type desc
    """
    country_iso = input("Enter the ISO country code (in CAPS): ")
    cursor = connect.cursor()
    cursor.execute(sql, (country_iso,))
    airports = cursor.fetchall()

    if airports:
        print(f"\nAirports in {country_iso}")
        for airport in airports:
            print(airport)
        print("HOW TO READ: airport size, name, municipality, icao code, iata code, elevation in feet, latitude, longitude")
        print("PRICES FOR AIRPORTS: small: 3,000,000; medium: 6,000,000; large: 12,000,000")
    else:
        print(f"No airports found for {country_iso}")

    cursor.close()
