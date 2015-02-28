import sqlite3

with sqlite3.connect('cc_database.db') as connection:
       c = connection.cursor()
       c.executescript("""
              drop table if exists user;
              create table user (
              id  integer primary key autoincrement,
              username text not null,
              password text not null,
              email text not null,
              phone integer,
              campus text not null,
              rating integer
       );
       drop table if exists dresses;
       create table dresses (
              id integer primary key autoincrement,
              size integer,
              color text not null,
              deposit real,
              rental real,
              image text not null
       );
       """)
