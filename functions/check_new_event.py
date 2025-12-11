import random


def check_new_event(connect, player):
    cursor = connect.cursor(buffered=True)

    cursor.execute("""
                   SELECT pe.id
                   FROM player_events pe
                            JOIN game g ON pe.game_id = g.id
                   WHERE g.name = %s
                   """, (player,))

    if cursor.fetchone():
        return 0


    luku = random.randint(1, 80)

    if luku > 5:
        return 0


    event_map = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4}
    event_id = event_map.get(luku)


    if event_id in [0, 1, 2, 4]:
        cursor.execute("""
                       SELECT COUNT(*)
                       FROM player_runway pr
                                JOIN player_airports pa ON pr.player_airports_id = pa.id
                                JOIN game g ON pa.game_id = g.id
                       WHERE g.name = %s
                         AND pr.status = 'operational'
                       """, (player,))

        runway_count = cursor.fetchone()[0]

        if runway_count == 0:
            return 0

    elif event_id == 3:
        cursor.execute("""
                       SELECT COUNT(*)
                       FROM player_terminal pt
                                JOIN player_airports pa ON pt.player_airports_id = pa.id
                                JOIN game g ON pa.game_id = g.id
                       WHERE g.name = %s
                         AND pt.status = 'operational'
                       """, (player,))

        terminal_count = cursor.fetchone()[0]

        if terminal_count == 0:
            return 0


    cursor.execute("SELECT * FROM event_types WHERE id = %s", (event_id,))
    event_data = cursor.fetchone()

    if not event_data:
        return 0

    otsikko = event_data[1]
    selite = event_data[2]

    if event_id == 4:
        cursor.execute("UPDATE game SET money = money + 1000000 WHERE name = %s", (player,))
        connect.commit()
        return 5, otsikko, selite

    duration = 0
    if event_id == 0:
        duration = 8
    elif event_id == 1:
        duration = 3
    elif event_id == 2:
        duration = 2
    elif event_id == 3:
        duration = 4

    cursor.execute("""
                   INSERT INTO player_events (game_id, event_types_id, event_weeks_left, original_yield)
                   VALUES ((SELECT id FROM game WHERE name = %s), %s, %s, 0)
                   """, (player, event_id, duration))

    connect.commit()

    return luku, otsikko, selite