import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from entity.model import *
from datetime import date
from dao.ICarLeaseRepository import ICarLeaseRepository
from exceptions.custom_exceptions import * 
from util.DBConnUtil import *


class ICarLeaseRepositoryImpl(ICarLeaseRepository):
   
   def __init__(self) -> None:
       self.conn=DBConnection.getConnection()
       self.cursor=self.conn.cursor()
       
   
   def add_car(self, Vehicle: Vehicle) -> None:
        try:
            self.cursor.execute("""
                INSERT INTO Vehicle VALUES(?, ?, ?, ?, ?, ?, ?);""", 
                (Vehicle.get_make(),Vehicle.get_model(), Vehicle.get_year(), 
                 Vehicle.get_daily_rate(), Vehicle.get_status(),Vehicle.get_passenger_capacity(), Vehicle.get_engine_capacity()))
            self.conn.commit()
            print("Vehicle Added Successfully!!\n")
        except Exception as e:
            self.conn.rollback()
            print("Error Occured,", str(e))
        finally:
           print("Select the Option From Below:")
            

   def remove_car(self, vehicle_id: int) -> None:
        try:
            self.cursor.execute("""
                DELETE FROM Vehicle
                WHERE vehicleID = ?
            """, (vehicle_id))
            if self.cursor.rowcount == 0:
                raise CarNotFoundException(vehicle_id)
            self.conn.commit()
            print("Vehicle Removed Successfully!!\n")
        except CarNotFoundException as e:
            print(e)
        except Exception as e:
            self. conn.rollback()
            print("Error Occured,", str(e))
        finally:
           print("Select the Option From Below:")


   def list_available_cars(self):
       try:
           available_cars = []
           self.cursor.execute("""SELECT * FROM Vehicle WHERE status = 'available';""")
           information = self.cursor.fetchall()
           for row in information:
                vehicle_id, make, model, year, daily_rate, status, passenger_capacity, engine_capacity = row
                vehicle = Vehicle(make=make, model=model, year=year, daily_rate=daily_rate, status=status, passenger_capacity=passenger_capacity, engine_capacity=engine_capacity, vehicle_id=vehicle_id)
                available_cars.append(vehicle)
           return available_cars
       except Exception as e:
                print("Error occurred while Fetching Available Cars,", str(e))
                return []
       finally:
            print("Select the Option From Below:")
    

   def list_rented_cars(self): 
        try:
             rented_cars = []
             self.cursor.execute("""
                    SELECT * FROM Vehicle WHERE status NOT IN ('available');""")
             for row in self.cursor.fetchall():
                    vehicle_id, make, model, year, daily_rate, status, passenger_capacity, engine_capacity = row
                    vehicle = Vehicle(make=make, model=model, year=year, daily_rate=daily_rate, status=status, passenger_capacity=passenger_capacity, engine_capacity=engine_capacity, vehicle_id=vehicle_id)
                    rented_cars.append(vehicle)
             return rented_cars
        except Exception as e:
                print("Error occurred while Fetching Not Available Cars,", str(e))
                return []
        finally:
            print("Select the Option From Below:")
        

   def find_car_by_id(self, Vehicle_id: int) -> Vehicle:
    try:
        self.cursor.execute("""SELECT * FROM Vehicle WHERE vehicleID = (?);""", (Vehicle_id))
        if self.cursor.rowcount == 0:
            raise CarNotFoundException(Vehicle_id)
        else:
            row = self.cursor.fetchone()
            vehicle_id, make, model, year, daily_rate, status, passenger_capacity, engine_capacity = row
            return Vehicle(make=make, model=model, year=year, daily_rate=daily_rate, status=status, passenger_capacity=passenger_capacity, engine_capacity=engine_capacity, vehicle_id=vehicle_id)      
    except CarNotFoundException as e:
        print(e)
    except Exception as e:
        print("Error occurred,", str(e))
        return None
    finally:
        print("Select the Option From Below:")

             
   def add_customer(self, customer: Customer) -> None:
        try:
              self.cursor.execute("""INSERT INTO Customer VALUES (?, ?, ?, ?);""", (customer.get_first_name(),customer.get_last_name(),customer.get_email(),customer.get_phone_number()))
              self.conn.commit()
              print("Customer Added Successfully!!\n")
        except Exception as e:
                self.conn.rollback()
                print("Error occurred,", str(e))
        finally:
            print("Select the Option From Below:")


   def remove_customer(self, customer_id: int) -> None:
        try:
            self.cursor.execute("""DELETE FROM Customer WHERE customerID = ?;""", (customer_id))
            if self.cursor.rowcount == 0:
                raise CustomerNotFoundException(customer_id)
            self.conn.commit()
            print("Customer Removed Successfully!!\n")
        except CustomerNotFoundException as e:
            print(e)
        except Exception as e:
                self.conn.rollback()
                print("Error occurred,", str(e))
        finally:
            print("Select the Option From Below:")
            

   def list_customers(self) -> list[Customer]:
        try:
            self.cursor.execute("""SELECT * FROM Customer;""")
            customers = []
            for row in self.cursor.fetchall():
                    customer_id, first_name, last_name, email, phone_number = row
                    customer = Customer(customer_id, first_name, last_name, email, phone_number)
                    customers.append(customer)
            return customers
        except Exception as e:
                print("Error occurred,", str(e))
                return []
        finally:
            print("Select the Option From Below:")

        
   def find_customer_by_id(self, customer_id: int) -> Customer:
        try:
            self.cursor.execute("""SELECT * FROM customer WHERE customerID = ?;""", (customer_id))  
            if self.cursor.rowcount == 0:
                raise CustomerNotFoundException(customer_id)
            else:
                row = self.cursor.fetchone()
                customer_id, first_name, last_name, email, phone_number = row
                return Customer(customer_id, first_name, last_name, email, phone_number)
        except CustomerNotFoundException as e:
            print(e)
        except Exception as e:
                print("Error occurred,", str(e))
                return None
        finally:
            print("Select the Option From Below:")

             
   def create_lease(self, lease:Lease) -> Lease:
        try:
            self.cursor.execute("""INSERT INTO Lease VALUES (?, ?, ?, ?, ?);""", (lease.get_vehicle_id(),lease.get_customer_id(),lease.get_start_date(),lease.get_end_date(),lease.get_type()))
            self.conn.commit()
            print("Lease Created Successfully!!\n")
        except Exception as e:
                self.conn.rollback()
                print("Error occurred,", str(e))
        finally:
            print("Select the Option From Below:")


   def return_car(self, lease_id: int) -> Lease:
        try:
            self.cursor.execute("""SELECT * FROM Lease WHERE leaseID = ?;""", (lease_id,))
            row = self.cursor.fetchone()
            if row is None:
                raise LeaseNotFoundException(lease_id)
            return row
        except LeaseNotFoundException as e:
            print(e)
        except Exception as e:
                self.conn.rollback()
                print("Error occurred,", str(e))
                return None

             
   def list_active_leases(self) -> list[Lease]:
        try:
             today = date.today()
             start_date = input("Enter Start Date (YYYY-MM-DD): ")
             self.cursor.execute("""SELECT * FROM Lease WHERE startDate = ?;""", (start_date))
             row=self.cursor.fetchall()
             return row
        except Exception as e:
                self.conn.rollback()
                print("Error occurred,", str(e))

             
   def list_lease_history(self) -> list[Lease]:
        try:
            self.cursor.execute("""SELECT * FROM Lease;""") 
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
                self.conn.rollback()
                print("Error occurred,", str(e))


   def record_payment(self, payment:Payment) -> None:
        try:
            self.cursor.execute("""INSERT INTO Payment VALUES (?, ?, ?);""", 
                (payment.get_lease_id(),payment.get_payment_date(),payment.get_amount()))
            self.conn.commit()
            print("Payment Recorded Successfully!!\n")
        except Exception as e:
                self.conn.rollback()
                print("Error occurred,", str(e))
        finally:
            print("Select the Option From Below:")

             
   def closeconn(self):
        if hasattr(self,'cursor'):
             self.cursor.close()
        if hasattr(self,'conn'):
             self.conn.close()


