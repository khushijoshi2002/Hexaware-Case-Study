# Hexaware Case Study Porject
Schema

CREATE TABLE Vehicle (
vehicleID INT PRIMARY KEY Identity(1,1),
make VARCHAR(50),
model VARCHAR(50),
year INT,
dailyRate DECIMAL(10, 2),
status VARCHAR(15) CHECK (status IN ('available', 'notAvailable')),
passengerCapacity INT,
engineCapacity DECIMAL(10, 2)
);


CREATE TABLE Customer (
customerID INT PRIMARY KEY identity(100,1),
firstName VARCHAR(50),
lastName VARCHAR(50),
email VARCHAR(100),
phoneNumber VARCHAR(15)
);


CREATE TABLE Lease (
leaseID INT PRIMARY KEY identity(300,1),
vehicleID INT FOREIGN KEY REFERENCES Vehicle(vehicleID),
customerID INT FOREIGN KEY REFERENCES Customer(customerID),
startDate DATE,
endDate DATE,
type VARCHAR(50) CHECK (type IN ('DailyLease', 'MonthlyLease'))
);


CREATE TABLE Payment (
paymentID INT PRIMARY KEY identity(1000,1),
leaseID INT FOREIGN KEY REFERENCES Lease(leaseID),
paymentDate DATE,
amount DECIMAL(10, 2)
);

