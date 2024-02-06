USE GST
GO

CREATE FUNCTION [dbo].[calcTotalPrice](@productId int,@qty int)
RETURNS decimal(4,2)
AS
BEGIN
    DECLARE @price decimal(4,2)
    DECLARE @totalPrice decimal(4,2)

    SELECT @price = [price] FROM [dbo].[PRODUCTS] where [productId] = @productId
    SELECT @totalPrice = @price * @qty

    RETURN @totalPrice
END