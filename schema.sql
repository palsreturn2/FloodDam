drop table if exists entries;
drop table if exists villages;
drop table if exists hospital;
create table entries (
  id integer primary key autoincrement,
  name varchar(30) not null,
  acquaintances number not null,
  settlement varchar(20) not null
);
create table villages(
name varchar(30) not null,
x varchar(30) not null,
y varchar(30) not null
);

insert into villages values("Mejhia","87.10700225830078","23.405630111694336");
insert into villages values("Gangajalghat","87.10700225830078","23.405630111694336");
insert into villages values("Kotulpur","87.59963989257812","22.925273895263672");
insert into villages values("Sonamukhi","87.41422271728516","23.343427658081055");
insert into villages values("Indas","87.62938690185547","23.142621994018555");
insert into villages values("Raipur","86.9598388671875","23.445419311523438");
insert into villages values("Sarenga","87.03074645996094","23.151464462280273");
insert into villages values("Simlapal","87.07135009765625","22.883113861083984");
insert into villages values("Taldangra","87.10647583007812","23.561573028564453");
insert into villages values("Saltora","86.93234252929688","22.662500381469727");

create table hospital(
name varchar(30) not null,
x varchar(30) not null,
y varchar(30) not null
);

insert into hospital values("0","86.85533905029297","22.974586486816406");
insert into hospital values("1","87.02354431152344","23.20586585998535");
insert into hospital values("2","87.31837463378906","23.065399169921875");
insert into hospital values("4","87.41422271728516","23.343427658081055");
