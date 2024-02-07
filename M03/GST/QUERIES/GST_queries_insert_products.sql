USE GST
GO

INSERT INTO PRODUCTS(PLU,productVendorId,price) VALUES
(3000,'1',2.00),
(3134,'1',2.20),
(3310,'1',1.50),
(3448,'1',3.10),
(3621,'1',1.60),
(4011,'2',2.80),
(4228,'2',5.10),
(4305,'2',4.40),
(4440,'2',3.80),
(4525,'2',0.90);

/* delete all rows, reseed:
DELETE FROM [dbo].[PRODUCTS]
DBCC CHECKIDENT ([PRODUCTS],RESEED,0)
SELECT * FROM [dbo].[PRODUCTS]
*/