CREATE TABLE IF NOT EXISTS article (
    id       SERIAL PRIMARY KEY NOT NULL,
    title    VARCHAR(255) NOT NULL,
    author   VARCHAR(255),
    date     TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    descript TEXT NOT NULL,
    article  TEXT UNIQUE NOT NULL
    );


CREATE TABLE IF NOT EXISTS analytics (
    ip          VARCHAR(255) PRIMARY KEY NOT NULL,
    platform    VARCHAR(255),
    browser     VARCHAR(255),
    city        VARCHAR(255),
    country     VARCHAR(255),
    continent   VARCHAR(255),
    bot         BOOLEAN DEFAULT FALSE,
    visits      INTEGER DEFAULT 0,
    created     TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_visit  TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );


CREATE TABLE IF NOT EXISTS mailing_list (
    email       VARCHAR(255) PRIMARY KEY NOT NULL,
    first_name  VARCHAR(255) NOT NULL,
    last_name   VARCHAR(255) NOT NULL,
    created     TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    downloaded  BOOLEAN DEFAULT FALSE
    );


CREATE TABLE IF NOT EXISTS free_beat (
    id          VARCHAR(5) PRIMARY KEY NOT NULL,
    url         VARCHAR(255) NOT NULL,
    locker      INTEGER,
    next        VARCHAR(17));
