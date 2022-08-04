drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title string not null,
  link string not null,
  date datetime not null,
  text string not null
);

drop table if exists entries2;
create table entries2 (
  id integer primary key autoincrement,
  title string not null,
  link string not null,
  date datetime not null,
  text string not null
);