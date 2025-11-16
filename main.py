import mysql.connector
import time
import threading
import queue
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

connect = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='flight_game',
         user='flight_game_user',
         password='1234',
         autocommit=True
         )


def create_game(g_money,g_time,g_name):
    sql = "INSERT INTO game (money,time,name) VALUES (%s,%s,%s)"
    cursor = connect.cursor()
    cursor.execute(sql, (g_money,g_time,g_name,))
    connect.commit()
    cursor.close()


player = input("Enter your name: ")
if not check_username(connect, player):
    money = 10000000
    week = 0
    create_game(money, week, player)
    print("")
    print("New game created")
    print("")
else:
    print("")
    print("Welcome back " + player + "!")
    print("")
    week = check_week(connect, player)

print("Enter your command here OR type 'commands' to view available commands ")

TICK_RATE = 0.1
TICK_TIME = 1 / TICK_RATE

paused = False
running = True
last = time.perf_counter()


player_input_queue = queue.Queue()

def get_input():
    while True:
        user_input = input("> ")
        player_input_queue.put(user_input)

input_thread = threading.Thread(target=get_input)
input_thread.start()


#pelin main-looppi:

while running:
    now = time.perf_counter()
    elapsed = now - last


    #asiat, jotka suoritetaan joka ticki:

    if not paused and elapsed >= TICK_TIME:
        last = now
        week += 1
        cursor = connect.cursor(buffered=True)
        cursor.execute("update game set time = %s where name = %s ", (week, player))
        connect.commit()
        cursor.close()
        constructions(connect)
        add_yield(connect, player)
        print ("")
        print(f"Week {check_week(connect, player)}")
        print("> ")


    if not player_input_queue.empty():
        player_input = player_input_queue.get()


        #seuraavat suoritetaan vain pelaajan käskystä:

        if player_input == "commands":
            available_commands = ["exit game", "pause", "resume", "view money", "view my airports", "view airports", "buy airports"]
            print("")
            print("Available commands:")
            print("")
            for command in available_commands:
                print(command)


        elif player_input == "exit game":
            connect.close()
            running = False


        elif player_input == "pause":
            paused = True
            print("Game paused")
            print("> ")


        elif player_input == "resume":
            paused = False
            print("Game resumed")
            print("> ")


        elif player_input == "view money":
            balance = give_bank_balance(connect, player)
            print(f"Your balance is: {balance:,}")

            if view_own_airports(connect, player):
                print(f"The total yield of your airports is: {get_player_yield(connect, player)}")


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


        elif player_input == "view airports":
            show_airports(connect)


        elif player_input == "buy airports":
            icao = input("Enter icao code of the airport you wish to purchase or type exit: ")

            if icao == "exit":
                continue

            else:
                buy_airport(icao, connect, player)


    time.sleep(0.1) #vähentää cpu-loadia, koska tarkistaa vain 0.1 sekunnin välein, onko 1 ticki kulunut