CREATE DATABASE GST;
GO;

USE GST;
GO

DROP TABLE [dbo].[CUSTOMERS]
CREATE TABLE [dbo].[CUSTOMERS] (
    [customerId]         INT           IDENTITY (1, 1) NOT NULL,
    [customerName]       VARCHAR (100) NOT NULL,
    [customerAddress]    VARCHAR (100) NOT NULL,
    [customerPostalCode] VARCHAR (5)   NOT NULL,
    [customerCity]       VARCHAR (50)  NOT NULL,
    [customerOIB]        CHAR (11)     NOT NULL,
    [customerWebsite]    VARCHAR (100) NOT NULL,
    PRIMARY KEY CLUSTERED ([customerId] ASC),
    CONSTRAINT [digitCustomerOIB] CHECK (NOT [customerOIB] like '%[^0-9]%'),
    CONSTRAINT [digitCustomerPC] CHECK (NOT [customerPostalCode] like '%[^0-9]%'),
    CONSTRAINT [lenCustomerOIB] CHECK (datalength([customerOIB])=(11)),
    CONSTRAINT [lenCustomerPC] CHECK (datalength([customerPostalCode])=(5))
);

DROP TABLE [dbo].[FTL]
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

DROP TABLE [dbo].[NONFTL]
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

DROP TABLE [dbo].[PRODUCTS]
CREATE TABLE [dbo].[PRODUCTS] (
    [productId]       INT            IDENTITY (1, 1) NOT NULL,
    [PLU]             INT            NOT NULL,
    [productVendorId] INT            NOT NULL,
    [price]           DECIMAL (4, 2) NOT NULL,
    CONSTRAINT [PK_PRODUCTS] PRIMARY KEY CLUSTERED ([productId] ASC),
    CONSTRAINT [digitPLU] CHECK (NOT [PLU] like '%[^0-9]%'),
    CONSTRAINT [lenPLU] CHECK (datalength([PLU])=(5)),
    CONSTRAINT [FK_PRODUCTS_FTL] FOREIGN KEY ([PLU]) REFERENCES [dbo].[FTL] ([PLU]),
    CONSTRAINT [FK_PRODUCTS_NONFTL] FOREIGN KEY ([PLU]) REFERENCES [dbo].[NONFTL] ([PLU]),
    CONSTRAINT [FK_PRODUCTS_VENDORS] FOREIGN KEY ([productVendorId]) REFERENCES [dbo].[VENDORS] ([vendorId])
);

DROP TABLE [dbo].[VENDORS]
CREATE TABLE [dbo].[VENDORS] (
    [vendorId]         INT           IDENTITY (1, 1) NOT NULL,
    [vendorName]       VARCHAR (100) NOT NULL,
    [vendorAddress]    VARCHAR (100) NOT NULL,
    [vendorPostalCode] VARCHAR (5)   NOT NULL,
    [vendorCity]       VARCHAR (50)  NOT NULL,
    [vendorOIB]        CHAR (11)     NOT NULL,
    [vendorWebsite]    VARCHAR (100) NOT NULL,
    CONSTRAINT [PK_VENDORS] PRIMARY KEY CLUSTERED ([vendorId] ASC),
    CONSTRAINT [digitVendorOIB] CHECK (NOT [vendorOIB] like '%[^0-9]%'),
    CONSTRAINT [digitVendorPC] CHECK (NOT [vendorPostalCode] like '%[^0-9]%'),
    CONSTRAINT [lenVendorOIB] CHECK (datalength([vendorOIB])=(11)),
    CONSTRAINT [lenVendorPC] CHECK (datalength([vendorPostalCode])=(5))
);

DROP TABLE [dbo].[INVENTORY]
CREATE TABLE [dbo].[INVENTORY] (
    [inventoryId] INT NOT NULL,
    [productId]   INT NOT NULL,
    [vendorId]    INT NOT NULL,
    [qtyInStock]  INT NOT NULL,
    [qtyReStock]  INT NOT NULL,
    CONSTRAINT [PK_INVENTORY] PRIMARY KEY CLUSTERED ([inventoryId] ASC),
    CONSTRAINT [FK_INVENTORY_FTL] FOREIGN KEY ([productId]) REFERENCES [dbo].[PRODUCTS] ([productId]),
    CONSTRAINT [FK_INVENTORY_VENDORS] FOREIGN KEY ([vendorId]) REFERENCES [dbo].[VENDORS] ([vendorId])
);
