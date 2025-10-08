# Tätä funktiota kutsutaan, kun command="next week"
# Lisää game.money:iin lentokentän yieldin

def add_yield(connect, player):
    cursor = connect.cursor()
    cursor.execute("select yield from player_airports where yield != 0")
    yields = cursor.fetchall()
    if yields:
        sum_yields = 0
        for y in yields:
            sum_yields += y[0]
        cursor.execute("update game set money = money + %s where name = %s", (sum_yields, player))