BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Deliveries PURGE';
EXCEPTION
    WHEN OTHERS THEN
        NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Orders PURGE';
EXCEPTION
    WHEN OTHERS THEN
        NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Restaurants PURGE';
EXCEPTION
    WHEN OTHERS THEN
        NULL;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE Users PURGE';
EXCEPTION
    WHEN OTHERS THEN
        NULL;
END;
/

CREATE TABLE Users (
 UserID INT PRIMARY KEY,
 UserName VARCHAR(50),
 City VARCHAR(50),
 AccountType VARCHAR(20));

INSERT INTO Users VALUES (1, 'Aman Verma', 'Delhi', 'Premium');
INSERT INTO Users VALUES (2, 'Riya Sen', 'Mumbai', 'Regular');

CREATE TABLE Restaurants (
 RestaurantID INT PRIMARY KEY,
 RestaurantName VARCHAR(100),
 Cuisine VARCHAR(50),
 Rating DECIMAL(2,1));

INSERT INTO Restaurants VALUES (101, 'Spice Symphony', 'North Indian', 4.5);
INSERT INTO Restaurants VALUES (102, 'Pizza Express', 'Italian', 3.9);

CREATE TABLE Orders (
 OrderID INT PRIMARY KEY,
 UserID INT,
 RestaurantID INT,
 BillAmount DECIMAL(10,2),
 OrderDate DATE,
 FOREIGN KEY (UserID) REFERENCES Users(UserID),
 FOREIGN KEY (RestaurantID) REFERENCES Restaurants(RestaurantID));

INSERT INTO Orders VALUES (501, 1, 101, 1200.00, DATE '2026-07-15');
INSERT INTO Orders VALUES (502, 2, 102, 450.00, DATE '2026-07-16');

CREATE TABLE Deliveries (
 DeliveryID INT PRIMARY KEY,
 OrderID INT,
 DeliveryStatus VARCHAR(20),
 DeliveryTimeMinutes INT,
 FOREIGN KEY (OrderID) REFERENCES Orders(OrderID));

INSERT INTO Deliveries VALUES (901, 501, 'Delivered', 25);
INSERT INTO Deliveries VALUES (902, 502, 'Delivered', 42);

SELECT
    u.UserName,
    r.RestaurantName,
    o.BillAmount
FROM Orders o
JOIN Users u ON o.UserID = u.UserID
JOIN Restaurants r ON o.RestaurantID = r.RestaurantID;

SELECT DISTINCT r.RestaurantName
FROM Restaurants r
JOIN Orders o ON r.RestaurantID = o.RestaurantID
JOIN Deliveries d ON o.OrderID = d.OrderID;

SELECT
    o.OrderID,
    u.UserName
FROM Orders o
JOIN Users u ON o.UserID = u.UserID
JOIN Deliveries d ON o.OrderID = d.OrderID
WHERE d.DeliveryTimeMinutes > 35;

SELECT
    u.UserName,
    SUM(o.BillAmount) AS TotalSpend
FROM Users u
JOIN Orders o ON u.UserID = o.UserID
GROUP BY u.UserName;

SELECT
    u.UserName,
    COUNT(o.OrderID) AS TotalOrders
FROM Users u
LEFT JOIN Orders o ON u.UserID = o.UserID
GROUP BY u.UserName;

SELECT
    r.RestaurantName,
    SUM(o.BillAmount) AS RevenueFromDelhi
FROM Restaurants r
JOIN Orders o ON r.RestaurantID = o.RestaurantID
JOIN Users u ON o.UserID = u.UserID
WHERE u.City = 'Delhi'
GROUP BY r.RestaurantName
HAVING SUM(o.BillAmount) > 5000;

SELECT
    r.RestaurantName,
    COUNT(d.DeliveryID) AS CancelledOrderCount
FROM Restaurants r
JOIN Orders o ON r.RestaurantID = o.RestaurantID
JOIN Deliveries d ON o.OrderID = d.OrderID
WHERE d.DeliveryStatus = 'Cancelled'
GROUP BY r.RestaurantName;

SELECT
    u.UserName,
    u.City
FROM Users u
JOIN Orders o ON u.UserID = o.UserID
WHERE o.BillAmount > (
    SELECT AVG(BillAmount) FROM Orders
);

SELECT
    r.Cuisine,
    AVG(d.DeliveryTimeMinutes) AS AvgDeliveryTime
FROM Restaurants r
JOIN Orders o ON r.RestaurantID = o.RestaurantID
JOIN Deliveries d ON o.OrderID = d.OrderID
GROUP BY r.Cuisine
HAVING AVG(r.Rating) > 4.0;

SELECT
    Cuisine,
    RestaurantName,
    OrderCount,
    RANK() OVER (PARTITION BY Cuisine ORDER BY OrderCount DESC) AS RestaurantRank
FROM (
    SELECT
        r.Cuisine,
        r.RestaurantName,
        COUNT(o.OrderID) AS OrderCount
    FROM Restaurants r
    LEFT JOIN Orders o ON r.RestaurantID = o.RestaurantID
    GROUP BY r.Cuisine, r.RestaurantName
) RestaurantOrderCounts
ORDER BY Cuisine, RestaurantRank;