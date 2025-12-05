# Tätä funktiota kutsutaan, kun command="next week"
#1. Pävitettää kiitoradan ja terminaalin construction_weeks_left ja status
#2. Kun construction_weeks_left saavuttaa luvun 0, lisätään terminal/runway_types_id:n
# mukainen sum_yield (=yield-operating_cost) player_airports.yield:iin


def constructions(connect):
    #Terminaalin construction_weeks_left vähennetään luvulla 1
    cursor = connect.cursor(buffered=True)
    cursor.execute("select 1 from player_terminal") #tarkistetaan, onko taulu tyhjä
    if cursor.fetchone():
        cursor.execute("""update player_terminal set construction_weeks_left = construction_weeks_left - 1 
                          where construction_weeks_left > 0""")
        #Kun terminaali on rakennettu (construction_weeks_left=0), lisätään yield player_airports:iin
        # ja päivitetään status='operational'
        cursor.execute("""select player_airports_id, terminal_types_id from player_terminal
        where construction_weeks_left = 0 and status='under_construction'""")
        results = cursor.fetchall()
        if cursor.rowcount > 0:
            print("Your terminal has finished constructions!")
            for result in results:
                player_airports_id = result[0]
                terminal_types_id = result[1]
                cursor.execute(
                    "select operating_cost, yield from terminal_types where id=%s",
                    (terminal_types_id,))
                costs = cursor.fetchone()
                # Päivitetään player_airports.yield
                sum_yield = costs[1] - costs[0]
                cursor.execute("UPDATE player_airports SET yield = yield + %s WHERE id = %s", (sum_yield, player_airports_id))
        cursor.execute("""update player_terminal
                          set status = 'operational'
                          where construction_weeks_left = 0 and status='under_construction'""")


    #Kiitorata:
    cursor.execute("select 1 from player_runway")  # tarkistetaan, onko taulu tyhjä
    if cursor.fetchone():
        cursor.execute("""update player_runway set construction_weeks_left = construction_weeks_left - 1 
                          where construction_weeks_left > 0""")
        cursor.execute("""select player_airports_id, runway_types_id from player_runway
        where construction_weeks_left = 0 and status='under_construction'""")
        results = cursor.fetchall()
        if cursor.rowcount > 0:
            print("Your runway has finished constructions!")
            for result in results:
                player_airports_id = result[0]
                runway_types_id = result[1]
                cursor.execute(
                    "select operating_cost, yield from runway_types where id=%s",
                    (runway_types_id,))
                costs = cursor.fetchone()
                # Päivitetään player_airports.yield
                sum_yield = costs[1] - costs[0]
                cursor.execute("UPDATE player_airports SET yield = yield + %s WHERE id = %s", (sum_yield, player_airports_id))
        cursor.execute("""update player_runway
                          set status = 'operational'
                          where construction_weeks_left = 0 and status='under_construction'""")
    connect.commit()
    cursor.close()