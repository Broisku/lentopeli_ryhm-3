def get_player_yield(connect, player):
    sql_terminal_yield = """SELECT SUM(terminal_types.yield) FROM terminal_types
    INNER JOIN player_terminal ON player_terminal.terminal_types_id = terminal_types.id
    INNER JOIN player_airports ON player_terminal.player_airports_id = player_airports.id
    INNER JOIN game ON player_airports.game_id = game.id
    WHERE game.name = %s"""
    cursor = connect.cursor(buffered=True)
    cursor.execute(sql_terminal_yield, (player,))
    terminal_yield = cursor.fetchone()[0]

    sql_runway_yield = """SELECT SUM(runway_types.yield)  FROM runway_types
    INNER JOIN player_runway ON player_runway.runway_types_id = runway_types.id
    INNER JOIN player_airports ON player_runway.player_airports_id = player_airports.id
    INNER JOIN game ON player_airports.game_id = game.id
    WHERE game.name = %s"""
    cursor.execute(sql_runway_yield, (player,))
    runway_yield = cursor.fetchone()[0]

    terminal_yield = terminal_yield or 0
    runway_yield = runway_yield or 0
    total_yield = runway_yield + terminal_yield
    cursor.close()
    return total_yield