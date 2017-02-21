drop table if exists XXSY_URTracker;
create table XXSY_URTracker (
	id serial not null primary key,
	revision int,
	url varchar(50),
	title text,
	state varchar(100),
	task varchar(50)
);

drop table if exists XXSY_SVNLog;
create table XXSY_SVNLog (
	revision int not null primary key,
	author varchar(20),
	svnDate varchar(50),
	log text
);

drop table if exists XXSY_Misc;
create table XXSY_Misc (
	id int not null primary key,
	value text
);

create or replace function insert_urtracker(_id int, _url varchar(50), _title text, _state varchar(100), _revision int, _task varchar(50))
returns integer as
$$
begin
if (select count(revision) from XXSY_URTracker where url = _url) = 0 then
insert into XXSY_URTracker (id, url, title, state, revision, task) values (_id, _url, _title, _state, _revision, _task);
return 1;
end if;
return 0;
end;
$$
language plpgsql;
