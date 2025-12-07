def give_bank_balance(connect, player):
    sql = "SELECT MONEY FROM GAME where name = %s"
    cursor = connect.cursor(buffered=True)
    cursor.execute(sql, (player,))
    balance = cursor.fetchone()
    cursor.close()
    return balance[0]