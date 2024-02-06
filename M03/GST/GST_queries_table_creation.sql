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
    [FSMA FTL]                    VARCHAR (10)  NOT NULL,
    [PLU]                         INT           NOT NULL,
    [CATEGORY]                    VARCHAR (50)  NOT NULL,
    [COMMODITY]                   VARCHAR (50)  NOT NULL,
    [VARIETY]                     VARCHAR (MAX) NULL,
    [SIZE]                        VARCHAR (50)  NULL,
    [MEASUREMENTS: NORTH AMERICA] VARCHAR (200) NULL,
    [MEASUREMENTS: REST OF WORLD] VARCHAR (100) NULL,
    [RESTRICTIONS / NOTES]        VARCHAR (250) NULL,
    [BOTANICAL NAME]              VARCHAR (100) NULL,
    [AKA]                         VARCHAR (MAX) NULL,
    [NOTES]                       VARCHAR (MAX) NULL,
    [REVISION DATE]               VARCHAR (50)  NULL,
    [DATE ADDED]                  VARCHAR (50)  NULL,
    [GPC]                         VARCHAR (20)  NULL,
    [IMAGE]                       VARCHAR (MAX) NULL,
    [IMAGE_SOURCE]                VARCHAR (MAX) NULL,
    CONSTRAINT [PK_FTL] PRIMARY KEY CLUSTERED ([PLU] ASC)
);

DROP TABLE [dbo].[NONFTL]
CREATE TABLE [dbo].[NONFTL] (
    [FSMA FTL]                    VARCHAR (10)  NOT NULL,
    [PLU]                         INT           NOT NULL,
    [CATEGORY]                    VARCHAR (50)  NOT NULL,
    [COMMODITY]                   VARCHAR (50)  NOT NULL,
    [VARIETY]                     VARCHAR (MAX) NULL,
    [SIZE]                        VARCHAR (50)  NULL,
    [MEASUREMENTS: NORTH AMERICA] VARCHAR (200) NULL,
    [MEASUREMENTS: REST OF WORLD] VARCHAR (100) NULL,
    [RESTRICTIONS / NOTES]        VARCHAR (250) NULL,
    [BOTANICAL NAME]              VARCHAR (100) NULL,
    [AKA]                         VARCHAR (MAX) NULL,
    [NOTES]                       VARCHAR (MAX) NULL,
    [REVISION DATE]               VARCHAR (50)  NULL,
    [DATE ADDED]                  VARCHAR (50)  NULL,
    [GPC]                         VARCHAR (20)  NULL,
    [IMAGE]                       VARCHAR (MAX) NULL,
    [IMAGE_SOURCE]                VARCHAR (MAX) NULL,
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
    CONSTRAINT [lenPLUmax] CHECK (datalength([PLU])<(6)),
    CONSTRAINT [lenPLUmin] CHECK (datalength([PLU])>(3)),
    CONSTRAINT [FK_PRODUCTS_FTL] FOREIGN KEY ([PLU]) REFERENCES [dbo].[FTL_JOINED] ([PLU]),
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
    [inventoryId] INT      NOT NULL,
    [productId]   INT      NOT NULL,
    [qtyInStock]  INT      NOT NULL,
    [qtyReStock]  INT      NOT NULL,
    [dateAdded]   DATETIME NOT NULL,
    CONSTRAINT [PK_INVENTORY] PRIMARY KEY CLUSTERED ([inventoryId] ASC),
    CONSTRAINT [FK_INVENTORY_FTL] FOREIGN KEY ([productId]) REFERENCES [dbo].[PRODUCTS] ([productId])
);


DROP TABLE [dbo].[FTL_JOINED]
CREATE TABLE [dbo].[FTL_JOINED] (
    [FSMA FTL]                    VARCHAR (10)  NOT NULL,
    [PLU]                         INT           NOT NULL,
    [CATEGORY]                    VARCHAR (50)  NOT NULL,
    [COMMODITY]                   VARCHAR (50)  NOT NULL,
    [VARIETY]                     VARCHAR (MAX) NULL,
    [SIZE]                        VARCHAR (50)  NULL,
    [MEASUREMENTS: NORTH AMERICA] VARCHAR (200) NULL,
    [MEASUREMENTS: REST OF WORLD] VARCHAR (100) NULL,
    [RESTRICTIONS / NOTES]        VARCHAR (250) NULL,
    [BOTANICAL NAME]              VARCHAR (100) NULL,
    [AKA]                         VARCHAR (MAX) NULL,
    [NOTES]                       VARCHAR (MAX) NULL,
    [REVISION DATE]               VARCHAR (50)  NULL,
    [DATE ADDED]                  VARCHAR (50)  NULL,
    [GPC]                         VARCHAR (20)  NULL,
    [IMAGE]                       VARCHAR (MAX) NULL,
    [IMAGE_SOURCE]                VARCHAR (MAX) NULL,
    CONSTRAINT [PK_FTL_JOINED] PRIMARY KEY CLUSTERED ([PLU] ASC)
);

CREATE TABLE [dbo].[ORDERS_VENDORS] (
    [orderId]    INT IDENTITY (1, 1) NOT NULL,
    [vendorId]   INT NOT NULL,
    [productId]  INT NOT NULL,
    [productQty] INT NOT NULL,
    [totalPrice] AS  ([dbo].[calcTotalPrice]([productId],[productQty])),
    CONSTRAINT [PK_ORDERS_VENDORS] PRIMARY KEY CLUSTERED ([orderId] ASC),
    CONSTRAINT [FK_ORDERS_VENDORS_PRODUCTS] FOREIGN KEY ([productId]) REFERENCES [dbo].[PRODUCTS] ([productId]),
    CONSTRAINT [FK_ORDERS_VENDORS_VENDORS] FOREIGN KEY ([vendorId]) REFERENCES [dbo].[VENDORS] ([vendorId])
);

CREATE TABLE [dbo].[ORDERS_CUSTOMERS] (
    [orderId]    INT IDENTITY (1, 1) NOT NULL,
    [customerId] INT NOT NULL,
    [productId]  INT NOT NULL,
    [productQty] INT NOT NULL,
    [totalPrice] AS  ([dbo].[calcTotalPrice]([productId],[productQty])),
    CONSTRAINT [PK_ORDERS] PRIMARY KEY CLUSTERED ([orderId] ASC),
    CONSTRAINT [FK_ORDERS_CUSTOMERS_CUSTOMERS] FOREIGN KEY ([customerId]) REFERENCES [dbo].[CUSTOMERS] ([customerId]),
    CONSTRAINT [FK_ORDERS_CUSTOMERS_PRODUCTS] FOREIGN KEY ([productId]) REFERENCES [dbo].[PRODUCTS] ([productId])
);