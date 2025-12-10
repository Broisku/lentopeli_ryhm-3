def view_own_airports(connect, player):
    cursor = connect.cursor(buffered=True)
    cursor.execute("""
            SELECT 
       airport.type,
       airport.name,
       airport.municipality,
       airport.gps_code,
       airport.iata_code,
       airport.elevation_ft,
       airport.latitude_deg,
       airport.longitude_deg,
       player_airports.yield,
       country.name AS country,
       MAX(player_runway.id) AS runway_id,
       MAX(player_runway.construction_weeks_left) AS runway_weeks,
       MAX(player_runway.status) AS runway_status,
       MAX(player_terminal.id) AS terminal_id,
       MAX(player_terminal.construction_weeks_left) AS terminal_weeks,
       MAX(player_terminal.status) AS terminal_status
FROM airport
JOIN country
    ON airport.iso_country = country.iso_country
JOIN player_airports
    ON airport.player_airports_id = player_airports.id
JOIN game
    ON player_airports.game_id = game.id
LEFT JOIN player_runway
    ON player_runway.player_airports_id = player_airports.id
LEFT JOIN player_terminal
    ON player_terminal.player_airports_id = player_airports.id
WHERE game.name = %s
GROUP BY airport.id;
            """, (player,))
    airports = cursor.fetchall()
    return airports