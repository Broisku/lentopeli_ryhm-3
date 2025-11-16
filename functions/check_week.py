def check_week(connect, player):
    cursor = connect.cursor(buffered=True)
    cursor.execute("select time from game where name = %s", (player,))
    result = cursor.fetchone()
    return result[0]