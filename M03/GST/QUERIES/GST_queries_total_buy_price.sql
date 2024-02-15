USE GST
GO

CREATE FUNCTION [dbo].[calcTotalBuyPrice](@productId int,@qty int)
RETURNS decimal(6,2)
AS
BEGIN
    DECLARE @buyPrice float
    DECLARE @totalPrice float

    SELECT @buyPrice = [buyPrice] FROM [dbo].[PRODUCTS] where [productId] = @productId
    SELECT @totalPrice = @buyPrice * @qty

    RETURN @totalPrice
END
GO
