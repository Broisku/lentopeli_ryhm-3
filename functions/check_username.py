def check_username(connect, player):
    cursor = connect.cursor()
    cursor.execute("select name from game where name = %s", (player,))
    cursor.fetchone()
    cursor.close()
    if cursor.rowcount == 0:
        return False
    else:
        return True