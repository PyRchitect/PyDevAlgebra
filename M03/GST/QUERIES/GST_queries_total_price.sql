USE GST
GO

CREATE FUNCTION [dbo].[calcTotalPrice](@productId int,@qty int)
RETURNS decimal(6,2)
AS
BEGIN
    DECLARE @price float
    DECLARE @totalPrice float

    SELECT @price = [price] FROM [dbo].[PRODUCTS] where [productId] = @productId
    SELECT @totalPrice = @price * @qty

    RETURN @totalPrice
END
GO
