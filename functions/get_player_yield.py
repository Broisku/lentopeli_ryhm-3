def get_player_yield(connect, player):
    cursor = connect.cursor()

    # Runways
    cursor.execute("""
                   SELECT COALESCE(SUM(rt.yield - rt.operating_cost), 0)
                   FROM player_runway pr
                            JOIN runway_types rt ON pr.runway_types_id = rt.id
                            JOIN player_airports pa ON pr.player_airports_id = pa.id
                            JOIN game g ON pa.game_id = g.id
                   WHERE g.name = %s
                     AND pr.status = 'operational'
                   """, (player,))
    runway_profit = cursor.fetchone()[0]

    cursor.execute("""
                   SELECT COALESCE(SUM(tt.yield - tt.operating_cost), 0)
                   FROM player_terminal pt
                            JOIN terminal_types tt ON pt.terminal_types_id = tt.id
                            JOIN player_airports pa ON pt.player_airports_id = pa.id
                            JOIN game g ON pa.game_id = g.id
                   WHERE g.name = %s
                     AND pt.status = 'operational'
                   """, (player,))
    terminal_profit = cursor.fetchone()[0]

    total_profit = runway_profit + terminal_profit


    cursor.execute("""
                   SELECT event_types_id
                   FROM player_events pe
                            JOIN game g ON pe.game_id = g.id
                   WHERE g.name = %s
                   """, (player,))

    event = cursor.fetchone()

    if event:
        event_id = event[0]

        if event_id == 0:
            total_profit = total_profit - 75000

        elif event_id == 1:
            total_profit = total_profit * 2

        elif event_id == 2:
            total_profit = 0

        elif event_id == 3:
            total_profit = total_profit / 2

    cursor.close()
    return int(total_profit)