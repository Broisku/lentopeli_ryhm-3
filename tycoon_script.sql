alter table airport
drop column local_code,
drop column home_link,
drop column wikipedia_link,
add constraint iso_country
foreign key (iso_country) references country(iso_country)
;
alter table country
drop column wikipedia_link
;
create table player_airports(
id int not null auto_increment,
yield int,
primary key (id)
);
create table other_airports(
id int not null auto_increment,
yield int,
primary key (id)
);
create table runway_types(
id int not null auto_increment,
length int,
cost int,
construction_time int,
operating_cost int,
yield int,
primary key (id)
);
create table terminal_types(
id int not null auto_increment,
size int,
cost int,
construction_time int,
operating_cost int,
yield int,
primary key (id)
);
create table player_runway(
player_airports_id int,
runway_types_id int,
primary key (player_airports_id, runway_types_id),
foreign key (player_airports_id) references player_airports(id),
foreign key (runway_types_id) references runway_types(id)
);
create table other_runway(
other_airports_id int,
runway_types_id int,
primary key (other_airports_id, runway_types_id),
foreign key (other_airports_id) references other_airports(id),
foreign key (runway_types_id) references runway_types(id)
);
create table player_terminal(
player_airports_id int,
terminal_types_id int,
primary key (player_airports_id, terminal_types_id),
foreign key (player_airports_id) references player_airports(id),
foreign key (terminal_types_id) references terminal_types(id)
);
create table other_terminal(
other_airports_id int,
terminal_types_id int,
primary key (other_airports_id, terminal_types_id),
foreign key (other_airports_id) references other_airports(id),
foreign key (terminal_types_id) references terminal_types(id)
);
create table game(
id int not null auto_increment,
money int,
time int,
name varchar(40),
player_airports_id int,
other_airports_id int,
primary key (id),
foreign key (player_airports_id) references player_airports(id),
foreign key (other_airports_id) references other_airports(id)
);
create table event_types(
id int primary key,
description varchar(100)
);