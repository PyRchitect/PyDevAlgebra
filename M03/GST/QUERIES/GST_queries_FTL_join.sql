USE GST
GO
/*
SELECT * INTO [dbo].[FTLin]
FROM [dbo].[FTL];
SELECT * INTO [dbo].[NONFTLin]
FROM [dbo].[NONFTL];

ALTER TABLE [dbo].[FTLin] ADD FTLtype VARCHAR(10)
ALTER TABLE [dbo].[NONFTLin] ADD FTLtype VARCHAR(10)

UPDATE [dbo].[FTLin] SET FTLtype = 'FTL'
UPDATE [dbo].[NONFTLin] SET FTLtype = 'NONFTL'

DROP TABLE FTLin;
DROP TABLE NONFTLin;

SELECT * INTO FTL_JOINED FROM FTLin UNION SELECT * FROM NONFTLin;
ALTER TABLE FTL_JOINED ADD PRIMARY KEY ([PLU])

SELECT [PLU],[CATEGORY],[COMMODITY],[FTLtype] FROM FTL_JOINED ORDER BY [PLU]
*/

SELECT * INTO FTL_JOINED FROM FTL UNION SELECT * FROM NONFTL;
ALTER TABLE FTL_JOINED ADD PRIMARY KEY ([PLU])
SELECT [FSMA FTL],[PLU],[CATEGORY],[COMMODITY] FROM [dbo].[FTL_JOINED] ORDER BY [PLU]