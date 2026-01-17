# FACTORY:
class Vehicle:
    def drive(self):
        pass
class Car(Vehicle):
    def drive(self):
        return "Driving a car"
class Bike(Vehicle):
    def drive(self):
        return "Riding a bike"
class VehicleFactory:
    @staticmethod
    def create_vehicle(vehicle_type):
        if vehicle_type == "car":
            return Car()
        elif vehicle_type == "bike":
            return Bike()
        else:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")

# Usage
vehicle = VehicleFactory.create_vehicle("car")
print(vehicle.drive())  # "Driving a car"