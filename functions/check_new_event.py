# tämä funktio arpoo, että tuleeko eventtiä, jos tulee se asettaa eventin vaikutukset tietokantaan

import random

def check_new_event(connect, player):
    return 1, "otsikko", "kuvaus"

    # tarkastetaan, onko pelaajalla tällä hetkellä eventtiä, jos on niin poistutaan funktiosta
    cursor = connect.cursor(buffered=True)
    cursor.execute("""
                   select player_events.id
                   from player_events
                            inner join game on player_events.game_id = game.id
                   where game.name = %s
                   """, (player,))
    result = cursor.fetchone()
    if result is not None:
        return 0

    luku = random.randint(1, 25)

    if luku > 5:
        return 0

    else:
        cursor.execute("select * from event_types")
        eventti = cursor.fetchall()

        if luku == 1:

            # haetaan kiitoradan status ja yieldi

            cursor.execute("""
                    select status, yield from player_runway inner join player_airports 
                    on player_runway.player_airports_id = player_airports.id
                    inner join game on player_airports.game_id = game.id
                    where game.name = %s
                    limit 1
            """, (player,))
            result = cursor.fetchone()
            if result is None:
                return 0 # pelaajalla ei ole yhtäkään kiitorataa


            status = result[0]
            if status == "under_construction":
                cursor.close()
                return 0 # meteoriitti ei iske kiitorataan joka ei ole vielä valmis

            org_yield = result[1]

            # talletetaan alkuperäinen yieldi sekä event_id tietokantaan
            cursor.execute("""
                           insert into player_events(game_id, original_yield, event_types_id)
                           values ((select id from game where game.name = %s), %s, %s)
                           """, (player, org_yield, 0))


            # päivitetään tietokantaan eventin pituus

            cursor.execute(""" 
                            update player_events inner join game on game_id = game.id
                           set event_weeks_left = 8
                           where game.name = %s
                                limit 1
                            """,(player,))



            # sitten itse efekti: kiitoradan yieldi -75 000
            cursor.execute("""update player_runway 
                    inner join player_airports on player_runway.player_airports_id = player_airports.id 
                    inner join game on player_airports.game_id = game.id 
                    set yield = -75000
                    where game.name = %s and player_runway.id = 1
                           """, (player,))

            otsikko = eventti[0][1]
            selite = eventti[0][2]

            # printataan pelaajalle mitä tapahtui
            return 1, otsikko, selite


        elif luku == 2:

            # haetaan kiitoradan status ja yieldi

            cursor.execute("""
                           select status, yield
                           from player_runway
                                    inner join player_airports
                                               on player_runway.player_airports_id = player_airports.id
                                    inner join game on player_airports.game_id = game.id
                           where game.name = %s limit 1
                           """, (player,))
            result = cursor.fetchone()
            if result is None:
                return  0 # pelaajalla ei ole yhtäkään kiitorataa

            status = result[0]
            if status == "under_construction":
                cursor.close()
                return  0 # ei voi olla turistirysää jos ei ole kiitorata valmis

            org_yield = result[1]

            # talletetaan alkuperäinen yieldi sekä event_id tietokantaan
            cursor.execute("""
                           insert into player_events(game_id, original_yield, event_types_id)
                           values ((select id from game where game.name = %s), %s, %s)
                           """, (player, org_yield, 1))


            # lisätään tietokantaan eventin pituus

            cursor.execute("""
                           update player_events inner join game on game_id = game.id
                           set event_weeks_left = 3
                           where game.name = %s
                               limit 1
                           """, (player,))



            # efekti: tuplataan pelaajan ensimmäisen lentokentän yieldi

            cursor.execute("""
                           update player_airports
                           inner join game on player_airports.game_id = game.id
                           set yield = yield * 2
                           where game.name = %s
                            limit 1
                           """, (player,))

            otsikko = eventti[1][1]
            selite = eventti[1][2]

            # printataan pelaajalle mitä tapahtui
            return 2, otsikko, selite



        elif luku == 3:

            # haetaan pelaajan ensimmäisen kiitoradan status ja yieldi

            cursor.execute("""
                           select status, yield
                           from player_runway
                                    inner join player_airports
                                               on player_runway.player_airports_id = player_airports.id
                                    inner join game on player_airports.game_id = game.id
                           where game.name = %s
                           limit 1
                           """, (player,))
            result = cursor.fetchone()
            if result is None:
                return 0 # pelaajalla ei ole yhtäkään kiitorataa

            status = result[0]
            if status == "under_construction":
                cursor.close()
                return 0 # ei vaikuta kiitorataan joka ei ole vielä valmis

            org_yield = result[1]

            # talletetaan alkuperäinen yieldi sekä event_id tietokantaan
            cursor.execute("""
                           insert into player_events(game_id, original_yield, event_types_id)
                           values ((select id from game where game.name = %s), %s, %s)
                           """, (player, org_yield, 2))


            # lisätään tietokantaan eventin pituus

            cursor.execute("""
                           update player_events inner join game on game_id = game.id
                           set event_weeks_left = 2
                           where game.name = %s
                               limit 1
                           """, (player,))


            # sitten efekti

            cursor.execute("""
                update player_runway inner join player_airports on player_airports_id = player_airports.id 
                inner join game on player_airports.game_id = game.id 
                set yield = 0
                where game.name = %s
                            """, (player,))

            otsikko = eventti[2][1]
            selite = eventti[2][2]

            # printataan pelaajalle mitä tapahtui
            return 3, otsikko, selite



        elif luku == 4:

            # haetaan pelaajan ensimmäisen terminaalin status ja yieldi

            cursor.execute("""
                           select status, yield
                           from player_terminal
                                    inner join player_airports
                                               on player_terminal.player_airports_id = player_airports.id
                                    inner join game on player_airports.game_id = game.id
                           where game.name = %s
                           limit 1
                           """, (player,))
            result = cursor.fetchone()
            if result is None:
                return 0 # pelaajalla ei ole yhtäkään terminaalia

            status = result[0]
            if status == "under_construction":
                cursor.close()
                return 0 # ei vaikuta terminaaliin joka ei ole vielä valmis

            org_yield = result[1]

            # talletetaan alkuperäinen yieldi sekä event_id tietokantaan
            cursor.execute("""
                           insert into player_events(game_id, original_yield, event_types_id)
                           values ((select id from game where game.name = %s), %s, %s)
                           """, (player, org_yield, 3))


            # lisätään tietokantaan eventin pituus 4 viikkoa

            cursor.execute("""
                           update player_events inner join game on game_id = game.id
                           set event_weeks_left = 4
                           where game.name = %s
                               limit 1
                           """, (player,))



            # efekti

            cursor.execute("""
                           update player_terminal inner join player_airports on player_airports_id = player_airports.id 
                            inner join game on player_airports.game_id = game.id 
                            set yield = %s / 2
                            where game.name = %s
                            """, (org_yield, player,))

            otsikko = eventti[3][1]
            selite = eventti[3][2]

            # printataan pelaajalle mitä tapahtui
            return 4, otsikko, selite



        elif luku == 5:

            # haetaan pelaajan ensimmäisen kiitoradan status

            cursor.execute("""
                           select status
                           from player_runway
                                    inner join player_airports
                                               on player_runway.player_airports_id = player_airports.id
                                    inner join game on player_airports.game_id = game.id
                           where game.name = %s
                               limit 1
                           """, (player,))
            result = cursor.fetchone()
            if result is None:
                return 0 # pelaajalla ei ole yhtäkään kiitorataa

            status = result[0]
            if status == "under_construction":
                cursor.close()
                return 0 # ei voi laskeutua kiitoradalle, joka ei ole vielä valmis


            cursor.execute("update game set money = money + 1000000 where name = %s",(player,))
            connect.commit()

            otsikko = eventti[4][1]
            selite = eventti[4][2]

            # printataan pelaajalle mitä tapahtui
            return 5, otsikko, selite

    connect.commit()
    cursor.close()