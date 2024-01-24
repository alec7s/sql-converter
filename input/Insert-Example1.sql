-- WHERE ContactName = 'Thomas Erichsen'
INSERT INTO Customers (CustomerName, ContactName, Address, City, PostalCode, Country)
VALUES ('Cardinal', 'Tom B. Erichsen', 'Skagen 21', 'Stavanger', '4006', 'Norway');

--WRONG CustomerName LIKE '%Robin'
INSERT INTO Customers (CustomerName, City, Country) --Test comment 1
VALUES ('Cardinal', 'Stavanger', 'Norway'); -- Another test comment

SELECT * FROM TABLE1;