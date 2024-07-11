create table search_criteria
(
	id integer primary key,
	make varchar(32),
	model varchar(32),
	variant varchar(32),
	min_year integer,
	max_year integer,
	gearbox varchar(32),
	fuel varchar(32),
	body varchar(32),
	doors integer,
	drivetrain varchar(32),
    keywords varchar(32)
);

create table sale_vehicle
(
	id integer primary key,
	search_criteria_id integer not null references search_criteria,
	date numeric not null,
	make varchar(32),
	price integer not null,
	year integer,
	body varchar(32),
	mileage integer,
	engine_size integer,
	power integer,
	gearbox varchar(32),
	fuel varchar(32),
	owners integer
);

