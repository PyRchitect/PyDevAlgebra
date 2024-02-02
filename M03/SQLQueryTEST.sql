/* 
CREATE DATABASE BLACKLIST;
GO
*/

/* 
USE BLACKLIST;
GO
*/

/* 
CREATE TABLE COMPANIES
(
VAT int PRIMARY KEY,
Company_Name varchar(30) NOT NULL,
Reason varchar(40),
);
GO
*/

/* 
INSERT INTO COMPANIES (VAT, Company_Name, Reason)
VALUES
	(45865764, 'Subphoto', 'Didnt pay'),
	(58610451, 'Mightsam', 'Rude behavior'),
	(12157320, 'Labipost', 'Didnt pay')
;
GO
*/

SELECT *
FROM COMPANIES
WHERE VAT=58610451
