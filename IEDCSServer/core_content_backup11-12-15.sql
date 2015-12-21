--
-- File generated with SQLiteStudio v3.0.6 on sex Dez 11 09:40:13 2015
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: core_content
CREATE TABLE core_content (
    contentID   INTEGER       NOT NULL
                              PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR (150) NOT NULL,
    fileName    VARCHAR (150) NOT NULL,
    filepath    VARCHAR (400) NOT NULL,
    pages       INTEGER       NOT NULL,
    restriction VARCHAR (150) NOT NULL,
    description VARCHAR (250) NOT NULL,
    createdOn   DATETIME      NOT NULL
);

INSERT INTO core_content (
                             contentID,
                             name,
                             fileName,
                             filepath,
                             pages,
                             restriction,
                             description,
                             createdOn
                         )
                         VALUES (
                             1,
                             'Death Note S01',
                             'DEATH_NOTE01_',
                             'storage/Death_Note_vol01/',
                             15,
                             'World',
                             'Death Note',
                             '2015-11-16 02:54:38.530502'
                         );

INSERT INTO core_content (
                             contentID,
                             name,
                             fileName,
                             filepath,
                             pages,
                             restriction,
                             description,
                             createdOn
                         )
                         VALUES (
                             2,
                             'Death Note S02',
                             'DEATH_NOTE01_',
                             'storage/Death_Note_vol02/',
                             14,
                             'World',
                             'Death Note',
                             '2015-11-16 02:55:21.799806'
                         );

INSERT INTO core_content (
                             contentID,
                             name,
                             fileName,
                             filepath,
                             pages,
                             restriction,
                             description,
                             createdOn
                         )
                         VALUES (
                             3,
                             'Bleach S01',
                             'Bleach_',
                             'storage/Bleach_Capitulo_651',
                             16,
                             'Portugal',
                             'Bleach',
                             '2015-11-16 02:56:02.407932'
                         );


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
