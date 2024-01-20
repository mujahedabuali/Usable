create database web;

use web;
CREATE TABLE content  (name VARCHAR(255));

CREATE TABLE site  (url VARCHAR(255));
select * from site;

create table bookmark(
name VARCHAR(60),
url VARCHAR(255)
);


ALTER TABLE content
ADD username  VARCHAR(255) ;
ALTER TABLE userdata
ADD INDEX idx_username (username);
ALTER TABLE content
ADD FOREIGN KEY ( username ) REFERENCES userdata(username);

ALTER TABLE site
ADD username  VARCHAR(255) ;
ALTER TABLE site
ADD FOREIGN KEY ( username ) REFERENCES userdata(username);

ALTER TABLE bookmark
ADD username  VARCHAR(255) ;
ALTER TABLE bookmark
ADD FOREIGN KEY ( username ) REFERENCES userdata(username);

create Table lastuser(
id int primary key,
username varchar(250) 
);
