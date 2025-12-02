import time
from abc import ABC, abstractmethod

class Runway:
    def __init__(self, name):
        self.name = name
        self.available = True

class Gate:
    def __init__(self, name):
        self.name = name
        self.available = True

class Airport:
    def __init__(self, code, name, city, country):
        self.code = code
        self.name = name
        self.city = city
        self.country = country
        self.runways = [Runway(f"RW{i}") for i in range(1,3)]
        self.gates = [Gate(f"G{i}") for i in range(1,6)]
        self.flights_schedule = []

    def is_runway_available(self):
        for rw in self.runways:
            if rw.available:
                return rw
        return None

    def assign_gate(self):
        for g in self.gates:
            if g.available:
                return g
        return None

class Aircraft:
    def __init__(self, registration, model, airline):
        self.registration = registration
        self.model = model
        self.airline = airline
        self.capacity = 180
        self.current_fuel = 100
        self.range = 1000

    def refuel(self, amount):
        self.current_fuel += amount
        print(f"{self.registration} refueled by {amount}")

    def can_fly_to(self, destination):
        return True

class FlightState(ABC):
    @abstractmethod
    def handle_event(self, flight, event):
        pass

class ScheduledState(FlightState):
    def handle_event(self, flight, event):
        if event == "boarding":
            flight.state = BoardingState()
            print(f"{flight.flight_number}: Boarding started")

class BoardingState(FlightState):
    def handle_event(self, flight, event):
        if event == "ready":
            flight.state = ReadyForDepartureState()
            print(f"{flight.flight_number}: Ready for departure")

class ReadyForDepartureState(FlightState):
    def handle_event(self, flight, event):
        if event == "taxi":
            flight.state = TaxiingState()
            print(f"{flight.flight_number}: Taxiing to runway")

class TaxiingState(FlightState):
    def handle_event(self, flight, event):
        if event == "takeoff":
            flight.state = TakeoffState()
            print(f"{flight.flight_number}: Taking off")

class TakeoffState(FlightState):
    def handle_event(self, flight, event):
        if event == "inflight":
            flight.state = InFlightState()
            print(f"{flight.flight_number}: In flight")

class InFlightState(FlightState):
    def handle_event(self, flight, event):
        if event == "landing":
            flight.state = LandingState()
            print(f"{flight.flight_number}: Landing")

class LandingState(FlightState):
    def handle_event(self, flight, event):
        if event == "arrived":
            flight.state = ArrivedState()
            print(f"{flight.flight_number}: Arrived")

class ArrivedState(FlightState):
    def handle_event(self, flight, event):
        pass

class Flight:
    def __init__(self, flight_number, origin, destination, aircraft):
        self.flight_number = flight_number
        self.origin = origin
        self.destination = destination
        self.aircraft = aircraft
        self.state = ScheduledState()
        self.passengers = []

    def event(self, action):
        self.state.handle_event(self, action)

class Observer(ABC):
    @abstractmethod
    def update(self, flight, message):
        pass

class PassengerNotifier(Observer):
    def update(self, flight, message):
        print(f"[PassengerNotifier] Flight {flight.flight_number}: {message}")

class AirportDisplay(Observer):
    def update(self, flight, message):
        print(f"[AirportDisplay] Flight {flight.flight_number}: {message}")

class FlightController:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.flights = []
        return cls._instance

    def schedule_flight(self, flight):
        self.flights.append(flight)
        print(f"Flight {flight.flight_number} scheduled")

class FlightFactory:
    @staticmethod
    def create_domestic(flight_number, origin, destination, aircraft):
        return Flight(flight_number, origin, destination, aircraft)

    @staticmethod
    def create_international(flight_number, origin, destination, aircraft):
        return Flight(flight_number, origin, destination, aircraft)

airport = Airport("JFK", "John F. Kennedy", "New York", "USA")
plane1 = Aircraft("N12345", "Boeing 737", "Delta")

flight = FlightFactory.create_domestic("DL101", airport, "LAX", plane1)

controller = FlightController()
controller.schedule_flight(flight)

passenger_notifier = PassengerNotifier()
airport_display = AirportDisplay()
observers = [passenger_notifier, airport_display]

for action in ["boarding", "ready", "taxi", "takeoff", "inflight", "landing", "arrived"]:
    flight.event(action)
    for obs in observers:
        obs.update(flight, f"Event: {action}")
