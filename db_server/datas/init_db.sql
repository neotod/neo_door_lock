PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS pass_hashes;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS reports;
DROP TABLE IF EXISTS api_tokens;

CREATE TABLE pass_hashes(
    id integer primary key,
    hash text not null,
    len integer not null
);

CREATE TABLE users(
    id integer primary key,
    name_ text not null,
    lastname text default null,
    username text not null unique,
    pass_hash_id integer not null unique,
    email text not null unique,
    phone integer default 0,
    constraint hash_id_fk foreign key(pass_hash_id) references pass_hashes(id)
);

CREATE TABLE events(
    id integer primary key,
    name_ text not null,
    text_ text not null
);

CREATE TABLE reports (
    id integer PRIMARY KEY ,
    event_id integer not null,
    date text default CURRENT_DATE ,
    time text DEFAULT CURRENT_TIME,
    more_info text DEFAULT NULL,
    constraint event_id_fk foreign key(event_id) references events(id)
);

CREATE TABLE api_tokens(
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token TEXT NOT NULL UNIQUE,
    CONSTRAINT user_id_fk FOREIGN KEY(user_id) REFERENCES users(id)
);


INSERT INTO events VALUES(1, 'lock_state_change','تغییر وضعیت قفل');
INSERT INTO events VALUES(2, 'user_login','ورود کاربر به بات');
INSERT INTO events VALUES(3, 'entry','ورود');
INSERT INTO events VALUES(4, 'user_change','تغییر کاربر');

INSERT INTO pass_hashes VALUES(1, 'd64ddcd5979fd920a8809276b82f419f9994c58e85d54cf842d3b5060212bba2','e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683');

INSERT INTO users VALUES(1, 'neotod',NULL,'neotod',1,'neotod@gmail.com', 0);

COMMIT;