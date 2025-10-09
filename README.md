flight_game on tycoon tyyppinen peli, jossa pelaaja voi ostaa, hallita sekä laajentaa lentokenttiä. Pelialueena toimii koko maailma.

Google slides -esitys: https://docs.google.com/presentation/d/1I-xyIwyjQkKNC5q3b_cKXESJnfo__7F8rOGcOQvtc18/edit?usp=sharing

Link to docs: https://docs.google.com/document/d/1aKimyoUgxhR9TuIQnhn2PMnNXQFy1S0_VO-FlOQaC70/edit?tab=t.0

## TODO:

-when going to "view my airports" it should show the yield of your airports

- TEHTY: add operating cost and yield of bought runway affect players money

-add total money spent to operating cost, and the total yield of your airports, and the total profit when selecting "view money"

- TEHTY: add option to buy terminals

- TEHTY: if player does not have any airports yet return to commands and print "you dont have airports yet"

## Database Installation:

open mariadb as root user

if database flight_game already exists:

drop database flight_game;

create database flight_game;

use flight_game

download tycoon_base.sql

type source in terminal and drag tycoon_base.sql to mariadb terminal
