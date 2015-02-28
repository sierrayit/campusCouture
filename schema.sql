drop table if exists user;
create table user (
       id  integer primary key autoincrement,
       username text not null,
       email text not null,
       phone integer,
       campus text not null,
       rating integer
);

drop table if exists dresses;
create table dresses (
       id integer primary key autoincrement;
       size integer,
       color text not null,
       deposit integer,
       rental integer
);