def view_own_airports(connect, player):
    cursor = connect.cursor(buffered=True)
    cursor.execute("select * from airports where name = %s", (player,))
    airports = cursor.fetchall()
    return airports