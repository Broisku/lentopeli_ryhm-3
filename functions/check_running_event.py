# tämä funktio tarkastaa, onko eventti loppunut, jos on se päättää eventin ja palauttaa arvot

def check_running_event(connect, player):

    # tarkastetaan, onko pelaajalla tällä hetkellä eventtiä
    cursor = connect.cursor(buffered=True)
    cursor.execute("""
                   select player_events.id from player_events
                    inner join game on player_events.game_id = game.id
                    where game.name = %s
                   """, (player,))
    result = cursor.fetchone()
    if result is None:
        return 0 # ei ole mitään, niin poistutaan funktiosta

    else: #tarkistetaan, kuinka monta viikkoa enää jäljellä
        cursor.execute("""
                        select event_weeks_left from player_events
                       inner join game on player_events.game_id = game.id
                       where game.name = %s
                       """, (player,))
        result = cursor.fetchone()[0]


        # vähennetään yksi viikko event_weeks_leftistä

        cursor.execute("""
                       update player_events inner join game
                       on player_events.game_id = game.id
                           set event_weeks_left = event_weeks_left - 1
                       where game.name = %s
                       """, (player,))


        if result == 0: # eventti on päättynyt ja pitäisi palauttaa alkutilanne. selvitetään mikä eventti oli kyseessä
            # haetaan myös vanha yieldi samalla
            cursor.execute("""
                           select event_types_id, original_yield from player_events
                           inner join game on player_events.game_id = game.id
                           where game.name = %s
                           """, (player,))
            result = cursor.fetchone()
            event_id = result[0]
            org_yieldi = result[1]


            # palautetaan alkutilanne käyden läpi mikä eventti oli kyseessä

            if event_id == 0:
                cursor.execute("""update player_runway
                                      inner join player_airports
                                  on player_runway.player_airports_id = player_airports.id
                                      inner join game on player_airports.game_id = game.id
                                      set yield = %s
                                  where game.name = %s
                                    limit 1
                               """, (org_yieldi, player,))


            elif event_id == 1:
                cursor.execute("""
                               update player_airports
                                   inner join game
                               on player_airports.game_id = game.id
                                   set yield = %s
                               where game.name = %s
                                   limit 1
                               """, (org_yieldi, player,))


            elif event_id == 2:
                cursor.execute("""
                               update player_runway inner join player_airports
                               on player_airports_id = player_airports.id
                                   inner join game on player_airports.game_id = game.id
                                   set yield = %s
                               where game.name = %s
                               """, (org_yieldi, player,))


            elif event_id == 3:
                cursor.execute("""
                               update player_terminal inner join player_airports
                               on player_airports_id = player_airports.id
                                   inner join game on player_airports.game_id = game.id
                                   set yield = %s
                               where game.name = %s
                               """, (org_yieldi, player,))


            # pyyhitään lopuksi player_events taulu

            cursor.execute("""
                           delete from player_events where game_id in (select id from game where name = %s)
                           """, (player,))

            return 2

        return 1


    connect.commit()
    cursor.close()