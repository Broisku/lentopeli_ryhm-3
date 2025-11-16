def create_game(connect, g_money,g_time,g_name):
    sql = "INSERT INTO game (money,time,name) VALUES (%s,%s,%s)"
    cursor = connect.cursor()
    cursor.execute(sql, (g_money,g_time,g_name,))