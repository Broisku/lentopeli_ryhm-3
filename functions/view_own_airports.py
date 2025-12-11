def view_own_airports(connect, player):
    cursor = connect.cursor()

    sql = """
          SELECT a.type, \
                 a.name, \
                 'dummy', \
                 a.gps_code, \
                 a.iata_code, \
                 'dummy', \
                 a.latitude_deg, \
                 a.longitude_deg, \
                 pa.yield, \
                 a.iso_country, \

                 \
                 (SELECT COUNT(*) FROM player_runway WHERE player_airports_id = pa.id), \

                  \
                 (SELECT COUNT(*) \
                  FROM player_runway \
                  WHERE player_airports_id = pa.id AND status = 'under_construction'), \

                 'operational', \

                  \
                 (SELECT COUNT(*) FROM player_terminal WHERE player_airports_id = pa.id), \

                 (SELECT COUNT(*) \
                  FROM player_terminal \
                  WHERE player_airports_id = pa.id AND status = 'under_construction'), \

                 'operational'

          FROM game g
                   JOIN player_airports pa ON g.id = pa.game_id
                   JOIN airport a ON pa.id = a.player_airports_id
          WHERE g.name = %s \
          """

    cursor.execute(sql, (player,))
    result = cursor.fetchall()
    cursor.close()
    return result