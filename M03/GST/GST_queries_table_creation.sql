CREATE DATABASE GST;
GO;

USE GST;
GO;

CREATE TABLE [dbo].[CUSTOMERS] (
    [customerId] INT           IDENTITY (1, 1) NOT NULL,
    [firstName]  VARCHAR (MAX) NULL,
    [lastName]   VARCHAR (MAX) NULL,
    PRIMARY KEY CLUSTERED ([customerId] ASC)
);

CREATE TABLE [dbo].[FTL] (
    [FSMA FTL]                    NVARCHAR (255) NOT NULL,
    [PLU]                         INT            NOT NULL,
    [CATEGORY]                    NVARCHAR (255) NOT NULL,
    [COMMODITY]                   NVARCHAR (255) NOT NULL,
    [VARIETY]                     NVARCHAR (255) NULL,
    [SIZE]                        NVARCHAR (255) NULL,
    [MEASUREMENTS: NORTH AMERICA] NVARCHAR (255) NULL,
    [MEASUREMENTS: REST OF WORLD] NVARCHAR (255) NULL,
    [RESTRICTIONS / NOTES]        NVARCHAR (255) NULL,
    [BOTANICAL NAME]              NVARCHAR (255) NULL,
    [AKA]                         NVARCHAR (255) NULL,
    [NOTES]                       NVARCHAR (255) NULL,
    [REVISION DATE]               NVARCHAR (255) NULL,
    [DATE ADDED]                  NVARCHAR (255) NULL,
    [GPC]                         NVARCHAR (255) NULL,
    [IMAGE]                       NVARCHAR (255) NULL,
    [IMAGE_SOURCE]                NVARCHAR (255) NULL,
    CONSTRAINT [PK_FTL] PRIMARY KEY CLUSTERED ([PLU] ASC)
);

CREATE TABLE [dbo].[INVENTORY] (
    [inventoryId] INT            NOT NULL,
    [itemNum]     INT            NOT NULL,
    [vendorId]    INT            NOT NULL,
    [price]       DECIMAL (4, 2) NOT NULL,
    [qtyInStock]  INT            NOT NULL,
    [qtyReStock]  INT            NOT NULL,
    CONSTRAINT [PK_INVENTORY] PRIMARY KEY CLUSTERED ([inventoryId] ASC),
    CONSTRAINT [FK_INVENTORY_FTL] FOREIGN KEY ([itemNum]) REFERENCES [dbo].[PRODUCTS] ([itemNum]),
    CONSTRAINT [FK_INVENTORY_VENDORS] FOREIGN KEY ([vendorId]) REFERENCES [dbo].[VENDORS] ([vendorId])
);

CREATE TABLE [dbo].[NONFTL] (
    [FSMA FTL]                    NVARCHAR (255) NOT NULL,
    [PLU]                         INT            NOT NULL,
    [CATEGORY]                    NVARCHAR (255) NOT NULL,
    [COMMODITY]                   NVARCHAR (255) NOT NULL,
    [VARIETY]                     NVARCHAR (255) NULL,
    [SIZE]                        NVARCHAR (255) NULL,
    [MEASUREMENTS: NORTH AMERICA] NVARCHAR (255) NULL,
    [MEASUREMENTS: REST OF WORLD] NVARCHAR (255) NULL,
    [RESTRICTIONS / NOTES]        NVARCHAR (255) NULL,
    [BOTANICAL NAME]              NVARCHAR (255) NULL,
    [AKA]                         NVARCHAR (255) NULL,
    [NOTES]                       NVARCHAR (255) NULL,
    [REVISION DATE]               NVARCHAR (255) NULL,
    [DATE ADDED]                  NVARCHAR (255) NULL,
    [GPC]                         NVARCHAR (255) NULL,
    [IMAGE]                       NVARCHAR (255) NULL,
    [IMAGE_SOURCE]                NVARCHAR (255) NULL,
    CONSTRAINT [PK_NONFTL] PRIMARY KEY CLUSTERED ([PLU] ASC)
);

CREATE TABLE [dbo].[PRODUCTS] (
    [itemNum] INT NOT NULL,
    [PLU]     INT NOT NULL,
    CONSTRAINT [PK_PRODUCTS] PRIMARY KEY CLUSTERED ([itemNum] ASC),
    CONSTRAINT [digitPLU] CHECK (NOT [PLU] like '%[^0-9]%'),
    CONSTRAINT [lenPLU] CHECK (datalength([PLU])=(5)),
    CONSTRAINT [FK_PRODUCTS_FTL] FOREIGN KEY ([PLU]) REFERENCES [dbo].[FTL] ([PLU]),
    CONSTRAINT [FK_PRODUCTS_NONFTL] FOREIGN KEY ([PLU]) REFERENCES [dbo].[NONFTL] ([PLU])
);

CREATE TABLE [dbo].[VENDORS] (
    [vendorId]         INT           IDENTITY (1, 1) NOT NULL,
    [vendorName]       VARCHAR (100) NOT NULL,
    [vendorAddress]    VARCHAR (100) NOT NULL,
    [vendorPostalCode] VARCHAR (5)   NOT NULL,
    [vendorCity]       VARCHAR (50)  NOT NULL,
    [vendorOIB]        CHAR (11)     NOT NULL,
    [vendorWebsite]    VARCHAR (100) NULL,
    CONSTRAINT [PK_VENDORS] PRIMARY KEY CLUSTERED ([vendorId] ASC),
    CONSTRAINT [digitOIB] CHECK (NOT [vendorOIB] like '%[^0-9]%'),
    CONSTRAINT [digitPC] CHECK (NOT [vendorPostalCode] like '%[^0-9]%'),
    CONSTRAINT [lenOIB] CHECK (datalength([vendorOIB])=(11)),
    CONSTRAINT [lenPC] CHECK (datalength([vendorPostalCode])=(5))
);
