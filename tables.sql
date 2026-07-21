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
