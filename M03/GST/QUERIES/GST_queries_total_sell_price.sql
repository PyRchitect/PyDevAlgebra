USE GST
GO

CREATE FUNCTION [dbo].[calcTotalSellPrice](@productId int,@qty int)
RETURNS decimal(6,2)
AS
BEGIN
    DECLARE @sellPrice float
    DECLARE @totalPrice float

    SELECT @sellPrice = [sellPrice] FROM [dbo].[PRODUCTS] where [productId] = @productId
    SELECT @totalPrice = @sellPrice * @qty

    RETURN @totalPrice
END
GO
