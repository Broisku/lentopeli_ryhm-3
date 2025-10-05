"""
Sisältö:
1. Tietokantayhteys
2. Funktiot
3. Pelin aloitus (esim. säännöt)
4. Pelin asetukset (tallennetaan tiedot, esim. aloitusraha, aika, pelaajan nimi yms)
5. Peli-loop
6. Pelin lopetus, kun loop keskeytetään
"""

# 1. Tietokantayhteys

import mysql.connector

from functions.buy_airport import buy_airport
from functions.check_username import check_username
from functions.show_airports import show_airports
from functions.check_time import check_time

connect = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='flight_game',
         user='flight_game_user',
         password='1234',
         autocommit=True
         )

# 2. Funktiot

def create_game(g_money,g_time,g_name):
    sql = "INSERT INTO game (money,time,name) VALUES (%s,%s,%s)"
    cursor = connect.cursor()
    cursor.execute(sql, (g_money,g_time,g_name))

def give_bank_balance(connect, player):
    sql = "SELECT MONEY FROM GAME where name = %s"
    cursor = connect.cursor(buffered=True)
    cursor.execute(sql, (player,))
    balance = cursor.fetchone()
    cursor.close()
    return balance[0]

#funktioita voi kait kutsua muistakin tiedostoista jotka on samassa repossa niin ei tarvi olla kaikki funktiot tässä samassa


# 4. Pelin asetukset


player = input("Enter your name: ")
if check_username(connect, player) == False:
    money = 10000000
    time = 0
    create_game(money, time, player)
    print("New game created")
else:
    print("Welcome back " + player + "!")
    time = check_time(connect, player)


while True:
    print(f"Week {check_time(connect, player)}")
    player_input = input("Enter your command or type commands to view possible commands")
    if player_input == "view airports":
        show_airports(connect)
    elif player_input == "buy airports":
        icao = input("Enter icao code of the airport you wish to purchase: ")
        buy_airport(icao, connect, player)
    elif player_input == "view money":
        balance = give_bank_balance(connect, player)
        print(f"Your balance is: {balance:,}")
    elif player_input == "next week":
        time = time + 1
        cursor = connect.cursor(buffered=True)
        cursor.execute("update game set time = %s where name = %s ", (time, player))
        cursor.close()
    elif player_input == "commands":
        print("Possible commands: next week, view money, view airports, buy airports")