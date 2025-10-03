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

connect = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='tycoon',
         user='user',
         password='password',
         autocommit=True
         )

# 2. Funktiot

def create_game(g_money,g_time,g_name):
    sql = "INSERT INTO game (money,time,name) VALUES (%s,%s,%s)"
    cursor = connect.cursor()
    cursor.execute(sql, (g_money,g_time,g_name))

# 4. Pelin asetukset
money = 10000000
time = 0
player = input("Syötä pelaajan nimi: ")
create_game(money, time, player)

