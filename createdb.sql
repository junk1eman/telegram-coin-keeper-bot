create table expense(
    id integer primary key,
    amount integer,
    created datetime,
    category TEXT,
    description text,
    raw_text text,
    user_id integer
    );

create table user_info(
    id integer primary key,
    first_name text,
    last_name text,
    username text,
    created datetime
    );




