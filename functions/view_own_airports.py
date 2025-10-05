def view_own_airports(connect, player):
    cursor = connect.cursor(buffered=True)
    cursor.execute("""
select type, airport.name, municipality, gps_code, iata_code, elevation_ft, latitude_deg, longitude_deg, yield
from airport
join player_airports
on airport.player_airports_id = player_airports.id
join game on game.player_airports_id = player_airports.id
where game.name = %s""", (player,))
    airports = cursor.fetchall()
    return airports