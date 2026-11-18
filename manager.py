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
    SoftwareFJError,
    DuplicateRecordError,
    RecordNotFoundError,
    InvalidInputError,
)
from logger import FileLogger


class ManagementSystem:
    """Manages clients, services, and bookings in memory with full exception handling."""

    def __init__(self):
        self._clients: List[Client] = []
        self._services: List[Service] = []
        self._bookings: List[Booking] = []
        self._load_default_services()
        FileLogger.log("SYSTEM", "ManagementSystem initialized with default service catalog.")

    def _load_default_services(self) -> None:
        """Populates initial services covering all three derived classes."""
        self.add_service(RoomBooking("RM-01", "Executive Conference Room (25 pax)", 50.0, 25))
        self.add_service(RoomBooking("RM-02", "Small Meeting Room (8 pax)", 30.0, 8))
        self.add_service(EquipmentRental("EQ-01", "4K Laser Projector", 20.0, "Audiovisual"))
        self.add_service(EquipmentRental("EQ-02", "High-Performance Workstation", 25.0, "Computing"))
        self.add_service(SpecializedConsulting("CS-01", "Cloud Architecture Consulting", 80.0, "Cloud"))
        self.add_service(SpecializedConsulting("CS-02", "Cybersecurity Audit", 95.0, "Security"))

    def add_service(self, service: Service) -> None:
        """Adds a new service to the catalog after checking for duplicates."""
        if any(s.code.lower() == service.code.lower() for s in self._services):
            raise DuplicateRecordError(f"Service code '{service.code}' already exists.")
        self._services.append(service)
        FileLogger.log("EVENT", f"Service added to catalog: {service.get_details()}")

    def register_client(self, client_id: str, full_name: str, email: str) -> Client:
        """Creates and stores a new client using try/except/else and exception chaining."""
        try:
            if any(c.client_id.lower() == client_id.strip().lower() for c in self._clients):
                raise DuplicateRecordError(f"Client ID '{client_id}' is already registered.")
            new_client = Client(client_id, full_name, email)
        except SoftwareFJError as err:
            FileLogger.log("ERROR", f"Client registration failed: {err}")
            # Exception chaining preserving original cause
            raise SoftwareFJError(f"Unable to register client '{client_id}'.") from err
        else:
            # Executed only if no exception occurred
            self._clients.append(new_client)
            FileLogger.log("EVENT", f"New client registered: {new_client}")
            return new_client

    def find_client_by_id(self, client_id: str) -> Client:
        for client in self._clients:
            if client.client_id.lower() == client_id.strip().lower():
                return client
        error_msg = f"Client ID '{client_id}' was not found."
        FileLogger.log("ERROR", error_msg)
        raise RecordNotFoundError(error_msg)

    def find_service_by_code(self, service_code: str) -> Service:
        for service in self._services:
            if service.code.lower() == service_code.strip().lower():
                return service
        error_msg = f"Service code '{service_code}' was not found."
        FileLogger.log("ERROR", error_msg)
        raise RecordNotFoundError(error_msg)

    def find_booking_by_id(self, booking_id: int) -> Booking:
        for booking in self._bookings:
            if booking.booking_id == booking_id:
                return booking
        error_msg = f"Booking #{booking_id} was not found."
        FileLogger.log("ERROR", error_msg)
        raise RecordNotFoundError(error_msg)

    @singledispatchmethod
    def create_booking(
        self, client_or_id, service_or_code, hours: int, tax_rate: float = 0.0, discount_rate: float = 0.0
    ) -> Booking:
        raise InvalidInputError("Unsupported parameter types for creating a booking.")

    @create_booking.register
    def _(
        self, client: Client, service: Service, hours: int, tax_rate: float = 0.0, discount_rate: float = 0.0
    ) -> Booking:
        """Overload 1: Creates and confirms a booking directly from objects."""
        booking_id = len(self._bookings) + 1
        new_booking = Booking(booking_id, client, service, hours, tax_rate, discount_rate)
        new_booking.confirm()
        self._bookings.append(new_booking)
        FileLogger.log(
            "EVENT",
            f"Booking #{booking_id} [{new_booking.status}] for {client.full_name} | Service: {service.code} | Total: ${new_booking.total_cost:.2f}",
        )
        return new_booking

    @create_booking.register
    def _(
        self, client_id: str, service_code: str, hours: int, tax_rate: float = 0.0, discount_rate: float = 0.0
    ) -> Booking:
        """Overload 2: Creates a booking by resolving IDs with try/except/finally."""
        try:
            client = self.find_client_by_id(client_id)
            service = self.find_service_by_code(service_code)
            return self.create_booking(client, service, hours, tax_rate, discount_rate)
        except SoftwareFJError as err:
            raise SoftwareFJError(f"Booking creation failed for client '{client_id}'.") from err
        finally:
            FileLogger.log("AUDIT", f"Booking attempt processed for Client ID='{client_id}', Service='{service_code}'.")

    def cancel_booking(self, booking_id: int) -> Booking:
        """Cancels an existing booking by ID."""
        booking = self.find_booking_by_id(booking_id)
        booking.cancel()
        FileLogger.log("EVENT", f"Booking #{booking_id} has been Cancelled.")
        return booking

    def run_10_operations_simulation(self) -> str:
        """Simulates 10 complete operations (valid & invalid clients, services, and bookings)."""
        FileLogger.log("SIMULATION", "=== STARTING 10-OPERATION SYSTEM SIMULATION ===")
        results = []

        operations = [
            ("1. Valid Client Registration (C-501)", lambda: self.register_client("C-501", "Carlos Mendez", "carlos@mail.com")),
            ("2. Valid Client Registration (C-502)", lambda: self.register_client("C-502", "Diana Torres", "diana@mail.com")),
            ("3. Invalid Client (Duplicate ID C-501)", lambda: self.register_client("C-501", "Duplicate User", "dup@mail.com")),
            ("4. Invalid Client (Malformed Email)", lambda: self.register_client("C-503", "Bad Email", "bademail.com")),
            ("5. Valid Service Creation (RM-03)", lambda: self.add_service(RoomBooking("RM-03", "Training Lab", 45.0, 15))),
            ("6. Invalid Service Creation (Negative Rate)", lambda: self.add_service(EquipmentRental("EQ-99", "Broken Cam", -10.0, "Video"))),
            ("7. Valid Booking with 19% Tax (C-501, RM-01)", lambda: self.create_booking("C-501", "RM-01", 3, 0.19, 0.0)),
            ("8. Valid Booking with 10% Discount (C-502, CS-01)", lambda: self.create_booking("C-502", "CS-01", 6, 0.0, 0.10)),
            ("9. Invalid Booking (Non-existent Client)", lambda: self.create_booking("C-999", "EQ-01", 2)),
            ("10. Cancel Booking #1 & Retry Invalid Double Cancel", lambda: (self.cancel_booking(1), self.cancel_booking(1))),
        ]

        for label, action in operations:
            try:
                action()
            except Exception as exc:
                results.append(f"[HANDLED ERROR] {label} -> {exc}")
            else:
                results.append(f"[SUCCESS] {label}")

        FileLogger.log("SIMULATION", "=== COMPLETED 10-OPERATION SYSTEM SIMULATION ===")
        return "\n".join(results)

    def get_all_clients(self) -> List[Client]:
        return list(self._clients)

    def get_all_services(self) -> List[Service]:
        return list(self._services)

    def get_all_bookings(self) -> List[Booking]:
        return list(self._bookings)