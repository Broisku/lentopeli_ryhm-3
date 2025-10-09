def give_bank_balance(connect, player):
    sql = "SELECT MONEY FROM GAME where name = %s"
    cursor = connect.cursor(buffered=True)
    cursor.execute(sql, (player,))
    balance = cursor.fetchone()

    sql_terminal_yield = """SELECT SUM(terminal_types.yield) FROM terminal_types
    INNER JOIN player_terminal ON player_terminal.terminal_types_id = terminal_types.id
    INNER JOIN player_airports ON player_terminal.player_airports_id = player_airports.id
    INNER JOIN game ON game.player_airports_id = player_airports.id
    WHERE game.name = %s"""
    cursor.execute(sql_terminal_yield, (player,))
    terminal_yield = cursor.fetchone()

    sql_runway_yield = """SELECT SUM(runway_types.yield)  FROM runway_types
    INNER JOIN player_runway ON player_runway.runway_types_id = runway_types.id
    INNER JOIN player_airports ON player_runway.player_airports_id = player_airports.id
    INNER JOIN game ON game.player_airports_id = player_airports.id
    WHERE game.name = %s"""
    cursor.execute(sql_runway_yield, (player,))
    runway_yield = cursor.fetchone()

    total_yield = runway_yield + terminal_yield

    cursor.close()
    return balance[0], total_yield


