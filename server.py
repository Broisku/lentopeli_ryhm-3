from flask import Flask, jsonify, request
import threading
import time
import mysql.connector
from flask_cors import CORS

from functions.get_bank_balance import give_bank_balance
from functions.get_player_yield import get_player_yield
from functions.check_week import check_week
from functions.add_yield import add_yield
from functions.constructions import constructions
from functions.view_own_airports import view_own_airports
from functions.buy_airport import buy_airport
from functions.fetchrunway import fetchrunway
from functions.buy_runway import buy_runway
from functions.buy_runway import buy_runway


app = Flask(__name__)
CORS(app)

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        port=3306,
        database='flight_game',
        user='flight_game_user',
        password='1234',
        autocommit=True
    )


#asetuksia: yksi ticki kuluu kymmenessä sekunnissa

paused = False
running = True

TICK_RATE = 0.1
TICK_TIME = 1 / TICK_RATE
player_name = None


# luodaan pelaaja:

def create_game(connect, player_name, money=10_000_000, week=0):
    cursor = connect.cursor()
    cursor.execute(
        "INSERT INTO game (name, money, time) VALUES (%s, %s, %s)",
        (player_name, money, week)
    )
    cursor.close()
    connect.commit()


@app.route("/create_player", methods=["POST"])
def create_player():
    data = request.json
    player = data.get("name")

    if not player:
        return jsonify({"error": "No player name provided"}), 400

    connect = get_connection()

    # Tarkistetaan, löytyykö nimeä jo tietokannasta
    cursor = connect.cursor()
    cursor.execute("select name from game where name = %s", (player,))

    if cursor.fetchone():
        cursor.close()
        connect.close()
        return jsonify({"message": "Player already exists"}), 200 #löytyi: poistuu funktiosta

    # ei löytynyt: luo uuden pelaajan
    create_game(connect, player)
    connect.close()

    return jsonify({"message": f"Player {player} created successfully"})

def game_loop():
    global player_name
    last = time.perf_counter()

    # pelin main-looppi:
    while running:
        if not player_name:
            time.sleep(0.1) # odottaa, että saa nimen
            continue

        now = time.perf_counter()
        elapsed = now - last

        # asiat, jotka suoritetaan joka ticki:
        if not paused and elapsed >= TICK_TIME:
            last = now

            connect = get_connection()

            current_week = check_week(connect, player_name)
            new_week = current_week + 1

            cursor = connect.cursor()
            cursor.execute(
                "update game set time = %s where name = %s",
                (new_week, player_name)
            )
            cursor.close()

            constructions(connect)
            add_yield(connect, player_name)

            connect.close()

        time.sleep(0.01) #vähentää cpu-loadia, koska tarkistaa vain 0.01 (eikä 0.000001 tms.) sekunnin välein, onko 1 ticki kulunut


threading.Thread(target=game_loop, daemon=True).start()


@app.route("/status/<player>")
def status(player):
    global player_name
    if not player_name:
        player_name = player

    connect = get_connection()
    week = check_week(connect, player)
    money = give_bank_balance(connect, player)
    profit = get_player_yield(connect, player)
    connect.close()

    return jsonify({
        "week": week,
        "money": money,
        "profit": profit
    })


# pause api

@app.route("/pause", methods=["POST"])
def pause():
    global paused
    paused = True
    return jsonify({"paused": True})

@app.route("/resume", methods=["POST"])
def resume():
    global paused
    paused = False
    return jsonify({"paused": False})


# nopeus api

@app.route("/set_speed/<mode>")
def set_speed(mode):
    global TICK_TIME

    if mode == "slow":
        TICK_TIME = 2.0
    else:
        TICK_TIME = 1 / TICK_RATE

    return jsonify({"speed": TICK_TIME})



# airport apit:

@app.route('/airports')
def airports():
    connect = get_connection()
    cursor = connect.cursor()
    cursor.execute("select * from airport")
    airports = cursor.fetchall()
    cursor.close()
    connect.close()
    return jsonify(airports)


# palauttaa omistetut lentokentät
@app.route('/airports/owned/<player>')
def owned_airports(player):
    connect = get_connection()
    own_airports = view_own_airports(connect, player)
    if not own_airports:
        connect.close()
        return jsonify([])
    else:
        connect.close()
        return jsonify(own_airports)


# api, joka palauttaa lentokentät, joihin pelaajalla on varaa
@app.route('/airports/afford/<player>')
def afford_airports(player):
    connect = get_connection()
    cursor = connect.cursor()
    balance = give_bank_balance(connect, player)

    if balance < 3_000_000:
        connect.close()
        return jsonify([])

    elif balance < 6_000_000:
        cursor.execute("select * from airport where type = 'small_airport'")
        airports = cursor.fetchall()
        cursor.close()
        connect.close()
        return jsonify(airports)

    elif balance < 12_000_000:
        cursor.execute("select * from airport where type in ('medium_airport', 'small_airport')")
        airports = cursor.fetchall()
        cursor.close()
        connect.close()
        return jsonify(airports)

    else:
        cursor.execute("select * from airport")
        airports = cursor.fetchall()
        cursor.close()
        connect.close()
        return jsonify(airports)

@app.route('/buyairports/<player>/<icao>')
def buyairports(player, icao):
    connect = get_connection()
    buy_airport(icao, connect, player)
    connect.close()
    return jsonify({'purchased': True})

# Tällä voi hakea monta kiitotietä on saatavilla (huom. tätä routea ei ole vielä käytetty main.js:ssä)
@app.route('/runways/<player>/<icao>')
def runways(player, icao):
    connect = get_connection()
    return jsonify({'runway': fetchrunway(connect, player, icao)})
@app.route('/buyrunway/<player>/<icao>')
def buyrunway(player, icao):
    connect = get_connection()
    return jsonify({'purchased': buy_runway(connect, player, icao)})
@app.route('/buyterminal/<player>/<icao>')
def buyterminal(player, icao):
    connect = get_connection()
    return jsonify({'purchased': buy_runway(connect, player, icao)})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)