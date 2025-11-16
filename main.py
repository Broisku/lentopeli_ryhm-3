import mysql.connector
import time
from functions.buy_airport import buy_airport
from functions.check_username import check_username
from functions.get_player_yield import get_player_yield
from functions.show_airports import show_airports
from functions.check_week import check_week
from functions.view_own_airports import view_own_airports
from functions.view_runways import view_runway
from functions.view_terminals import view_terminal
from functions.get_bank_balance import give_bank_balance
from functions.add_yield import add_yield
from functions.constructions import constructions
from functions.create_game import create_game

connect = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='flight_game',
         user='flight_game_user',
         password='1234',
         autocommit=True
         )



player = input("Enter your name: ")
if not check_username(connect, player):
    money = 10000000
    week = 0
    create_game(connect, money, week, player)
    print("New game created")
else:
    print("Welcome back " + player + "!")
    week = check_week(connect, player)


TICK_RATE = 0.1
TICK_TIME = 1 / TICK_RATE

running = True
last = time.perf_counter()



while running:
    now = time.perf_counter()
    elapsed = now - last

    if elapsed >= TICK_TIME:
        last = now

         "update game set time += 1 where name = %s"
        constructions(connect)
        add_yield(connect, player)

        print(f"Week {check_week(connect, player)}")

        player_input = input("Enter your command or type commands to view available commands ")

        if player_input == "view airports":
            show_airports(connect)


        elif player_input == "buy airports":
            icao = input("Enter icao code of the airport you wish to purchase or type exit: ")

            if icao == "exit":
                continue

            else:
                buy_airport(icao, connect, player)


        elif player_input == "view money":
            balance = give_bank_balance(connect, player)
            print(f"Your balance is: {balance:,}")

            if view_own_airports(connect, player):
                print(f"The total yield of your airports is: {get_player_yield(connect, player)}")


        elif player_input == "commands":
            available_commands = ["exit game", "next week", "view money", "view airports", "view my airports", "buy airports"]
            print("Available commands:")
            for command in available_commands:
                print(command)


        elif player_input == "exit game":
            connect.close()
            break


        elif player_input == "view my airports":
            own_airports = view_own_airports(connect, player)

            if not own_airports:
                print("You dont have airports yet")

            else:
                print("Your airports:")
                print(
                    "HOW TO READ: airport size, name, municipality, icao code, iata code, elevation in feet, latitude, longitude, yield")
                for airport in own_airports:
                    print(airport)

                player_input = input("type upgrades to view available upgrades or type exit ")

                if player_input == "exit":
                    continue

                elif player_input == "upgrades":
                    runway_terminal = input(
                        "type runways to view available runways or type terminals to view available terminals or type exit ")

                    if runway_terminal == "exit":
                        continue

                    elif runway_terminal == "runways":
                        icao = input("Enter icao of your airport ")
                        view_runway(connect, player, icao)

                    elif runway_terminal == "terminals":
                        icao = input("Enter icao of your airport ")
                        view_terminal(connect, player, icao)