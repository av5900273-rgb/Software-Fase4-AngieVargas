from functools import singledispatchmethod
from typing import List
from models import (
    Client,
    Service,
    RoomBooking,
    EquipmentRental,
    SpecializedConsulting,
    Booking,
)
from exceptions import (
    DuplicateRecordError,
    RecordNotFoundError,
    InvalidInputError,
)
from logger import FileLogger


class ManagementSystem:
    """Manages clients, services, and bookings in memory using internal lists."""

    def __init__(self):
        # Initialize internal lists to store data in memory (no database used)
        self._clients: List[Client] = []
        self._services: List[Service] = []
        self._bookings: List[Booking] = []

        # Preload default catalog of services for Software FJ
        self._load_default_services()
        FileLogger.log("SYSTEM", "ManagementSystem initialized with default service catalog.")

    def _load_default_services(self) -> None:
        """Populates initial services covering all three derived classes."""
        self._services.append(RoomBooking("RM-01", "Executive Conference Room (25 pax)", 50.0, 25))
        self._services.append(RoomBooking("RM-02", "Small Meeting Room (8 pax)", 30.0, 8))
        self._services.append(EquipmentRental("EQ-01", "4K Laser Projector", 20.0, "Audiovisual"))
        self._services.append(EquipmentRental("EQ-02", "High-Performance Workstation", 25.0, "Computing"))
        self._services.append(SpecializedConsulting("CS-01", "Cloud Architecture Consulting", 80.0, "Cloud"))
        self._services.append(SpecializedConsulting("CS-02", "Cybersecurity Audit", 95.0, "Security"))

    def register_client(self, client_id: str, full_name: str, email: str) -> Client:
        """Creates and stores a new client after checking for duplicate IDs."""
        # Check if a client with the same ID already exists
        if any(c.client_id.lower() == client_id.strip().lower() for c in self._clients):
            error_msg = f"Client with ID '{client_id}' is already registered."
            FileLogger.log("ERROR", error_msg)
            raise DuplicateRecordError(error_msg)

        # Create Client instance (triggers setter validations)
        new_client = Client(client_id, full_name, email)
        self._clients.append(new_client)
        FileLogger.log("EVENT", f"New client registered: {new_client}")
        return new_client

    def find_client_by_id(self, client_id: str) -> Client:
        """Searches for a client by ID or raises RecordNotFoundError."""
        for client in self._clients:
            if client.client_id.lower() == client_id.strip().lower():
                return client
        error_msg = f"Client ID '{client_id}' was not found."
        FileLogger.log("ERROR", error_msg)
        raise RecordNotFoundError(error_msg)

    def find_service_by_code(self, service_code: str) -> Service:
        """Searches for a service by code or raises RecordNotFoundError."""
        for service in self._services:
            if service.code.lower() == service_code.strip().lower():
                return service
        error_msg = f"Service code '{service_code}' was not found."
        FileLogger.log("ERROR", error_msg)
        raise RecordNotFoundError(error_msg)

    # --- METHOD OVERLOADING IMPLEMENTATION ---
    @singledispatchmethod
    def create_booking(self, client_or_id, service_or_code, hours: int) -> Booking:
        """Base overloaded method signature for registering a service booking."""
        raise InvalidInputError("Unsupported parameter types for creating a booking.")

    @create_booking.register
    def _(self, client: Client, service: Service, hours: int) -> Booking:
        """Overload 1: Registers a booking directly using Client and Service objects."""
        booking_id = len(self._bookings) + 1
        new_booking = Booking(booking_id, client, service, hours)
        self._bookings.append(new_booking)
        FileLogger.log(
            "EVENT",
            f"Booking #{booking_id} created for {client.full_name} | Service: {service.code} | Total: ${new_booking.total_cost:.2f}",
        )
        return new_booking

    @create_booking.register
    def _(self, client_id: str, service_code: str, hours: int) -> Booking:
        """Overload 2: Registers a booking by looking up Client ID and Service Code strings."""
        client = self.find_client_by_id(client_id)
        service = self.find_service_by_code(service_code)
        # Delegate creation to Overload 1
        return self.create_booking(client, service, hours)

    # --- GETTERS FOR UI DISPLAY ---
    def get_all_clients(self) -> List[Client]:
        """Returns a copy of the registered clients list."""
        return list(self._clients)

    def get_all_services(self) -> List[Service]:
        """Returns a copy of the available services list."""
        return list(self._services)

    def get_all_bookings(self) -> List[Booking]:
        """Returns a copy of all confirmed bookings."""
        return list(self._bookings)