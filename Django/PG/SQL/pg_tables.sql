drop table if exists XXSY_URTracker;
create table XXSY_URTracker (
	id serial not null primary key,
	revision int,
	url varchar(50),
	title varchar(100),
	state varchar(20),
	task varchar(50)
);

drop table if exists XXSY_SVNLog;
create table XXSY_SVNLog (
	revision int not null primary key,
	author varchar(20),
	svnDate varchar(50),
	log text
);
