import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)
import unittest
from dao.ICarLeaseRepositoryImpl import ICarLeaseRepositoryImpl
from entity.model import Vehicle,Lease  
from exceptions.custom_exceptions import CarNotFoundException,LeaseNotFoundException,CustomerNotFoundException 


class TestCarRentalSystem(unittest.TestCase):
    def setUp(self):
        self.service_provider = ICarLeaseRepositoryImpl()
    
    def test_create_car(self):
        make = input("Enter Company Name: ")
        model = input("Enter Model: ")
        year = int(input("Enter Year: "))
        daily_rate = float(input("Enter Daily Rate: "))
        status = input("Enter Status (available, notAvailable): ")
        passenger_capacity = int(input("Enter Passenger Capacity: "))
        engine_capacity = float(input("Enter Engine Capacity: ")) 
        car = Vehicle(make=make, model=model, year=year, daily_rate=daily_rate, status=status, passenger_capacity=passenger_capacity, engine_capacity=engine_capacity)
        car_id = self.service_provider.add_car(car)
        self.assertIsNone(car_id)  


    def test_create_lease(self):
        customer_id = int(input("Enter Customer ID: "))
        vehicle_id = int(input("Enter Vehicle ID: "))
        start_date = input("Enter Start Date (YYYY-MM-DD): ")
        end_date = input("Enter End Date (YYYY-MM-DD): ")
        type=input("Enter Type('DailyLease', 'MonthlyLease'): ")
        lease=Lease(customer_id=customer_id,vehicle_id=vehicle_id,start_date=start_date,end_date=end_date,type=type)
        l=self.service_provider.create_lease(lease)
        self.assertIsNone(l)


    def test_retrieve_lease(self):
        lease_id = 301
        retrieved_lease = self.service_provider.return_car(lease_id)
        self.assertIsNotNone(retrieved_lease)


    def test_customer_not_found_exception(self):
        try:
            self.service_provider.find_customer_by_id(888)
        except CustomerNotFoundException as e:
            print("CustomerNotFoundException was raised:", e)

        
    def test_car_not_found_exception(self):
        try:
             self.service_provider.find_car_by_id(888) 
        except CarNotFoundException:
            print("CarNotFound Exception is  raised!!") 


    def test_lease_not_found_exception(self):
        try:
            self.service_provider.return_car(888)
        except LeaseNotFoundException:
            print("LeaseNotFound Exception is raised!!")

if __name__ == '__main__':
    unittest.main()
