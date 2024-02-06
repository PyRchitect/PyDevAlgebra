USE GST
GO
/*
INSERT INTO ORDERS_VENDORS(vendorId,productId,productQty) VALUES
(1,5,100),
(1,10,60),
(1,2,20),
(1,4,200),
(1,7,150),
(2,10,120),
(2,1,70),
(2,9,300),
(2,8,50),
(2,3,30);

SELECT * FROM ORDERS_VENDORS
*/

INSERT INTO ORDERS_CUSTOMERS(customerId,productId,productQty) VALUES
(1,5,10),
(1,10,20),
(1,2,10),
(1,4,50),
(1,7,50),
(2,10,20),
(2,1,10),
(2,9,50),
(2,8,10),
(2,3,10);

SELECT * FROM ORDERS_CUSTOMERS