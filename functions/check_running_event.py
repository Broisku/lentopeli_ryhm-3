def check_running_event(connect, player):
    cursor = connect.cursor(buffered=True)

    cursor.execute("""
                   SELECT pe.id, pe.event_weeks_left
                   FROM player_events pe
                            JOIN game g ON pe.game_id = g.id
                   WHERE g.name = %s
                   """, (player,))

    result = cursor.fetchone()

    if not result:
        return 0

    weeks_left = result[1]

    cursor.execute("""
                   UPDATE player_events pe
                       JOIN game g
                   ON pe.game_id = g.id
                       SET pe.event_weeks_left = pe.event_weeks_left - 1
                   WHERE g.name = %s
                   """, (player,))

    if weeks_left <= 1:
        cursor.execute("""
            DELETE pe FROM player_events pe
            JOIN game g ON pe.game_id = g.id
            WHERE g.name = %s
        """, (player,))

        connect.commit()
        return 2
    connect.commit()
    return 1