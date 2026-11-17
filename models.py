from abc import ABC, abstractmethod
from exceptions import InvalidInputError


class Client:
    """Represents a client with encapsulated attributes and strict data validation."""

    def __init__(self, client_id: str, full_name: str, email: str):
        # Use property setters to enforce validation rules upon creation
        self.client_id = client_id
        self.full_name = full_name
        self.email = email

    @property
    def client_id(self) -> str:
        # Getter for private client_id attribute
        return self._client_id

    @client_id.setter
    def client_id(self, value: str) -> None:
        # Validate that client ID is not empty or whitespace
        if not value or not value.strip():
            raise InvalidInputError("Client ID cannot be empty.")
        self._client_id = value.strip()

    @property
    def full_name(self) -> str:
        # Getter for private full_name attribute
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        # Validate that client name is not empty
        if not value or not value.strip():
            raise InvalidInputError("Client full name is required.")
        self._full_name = value.strip()

    @property
    def email(self) -> str:
        # Getter for private email attribute
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        # Validate basic email structure containing '@' and '.'
        if not value or "@" not in value or "." not in value:
            raise InvalidInputError("Invalid email address format.")
        self._email = value.strip()

    def __str__(self) -> str:
        # String representation of the client object
        return f"{self.client_id} - {self.full_name} ({self.email})"


class Service(ABC):
    """Abstract base class defining the common structure for all Software FJ services."""

    def __init__(self, code: str, description: str, base_rate: float):
        # Validate code and description are not empty
        if not code or not code.strip():
            raise InvalidInputError("Service code cannot be empty.")
        if not description or not description.strip():
            raise InvalidInputError("Service description cannot be empty.")
        # Validate base rate is strictly positive
        if base_rate <= 0:
            raise InvalidInputError("Base rate must be greater than zero.")

        self._code = code.strip()
        self._description = description.strip()
        self._base_rate = float(base_rate)

    @property
    def code(self) -> str:
        return self._code

    @property
    def description(self) -> str:
        return self._description

    @property
    def base_rate(self) -> float:
        return self._base_rate

    @abstractmethod
    def calculate_total_cost(self, hours: int) -> float:
        """Abstract method to be overridden by subclasses using polymorphism."""
        pass

    def get_details(self) -> str:
        """Returns a formatted summary of the service."""
        return f"[{self.code}] {self.description} - Base Rate: ${self.base_rate:.2f}/hr"


class RoomBooking(Service):
    """Derived class for meeting or conference room bookings."""

    def __init__(self, code: str, description: str, base_rate: float, capacity: int):
        # Call parent constructor
        super().__init__(code, description, base_rate)
        # Validate room capacity
        if capacity <= 0:
            raise InvalidInputError("Room capacity must be at least 1 person.")
        self.capacity = capacity

    def calculate_total_cost(self, hours: int) -> float:
        # Polymorphic calculation: adds a 10% surcharge for large rooms (> 20 people)
        subtotal = self.base_rate * hours
        return subtotal * 1.10 if self.capacity > 20 else subtotal


class EquipmentRental(Service):
    """Derived class for technological or audiovisual equipment rentals."""

    def __init__(self, code: str, description: str, base_rate: float, equipment_type: str):
        # Call parent constructor
        super().__init__(code, description, base_rate)
        if not equipment_type or not equipment_type.strip():
            raise InvalidInputError("Equipment type is required.")
        self.equipment_type = equipment_type.strip()

    def calculate_total_cost(self, hours: int) -> float:
        # Polymorphic calculation: adds a flat $15.00 insurance fee per rental
        return (self.base_rate * hours) + 15.0


class SpecializedConsulting(Service):
    """Derived class for specialized software and IT consulting services."""

    def __init__(self, code: str, description: str, base_rate: float, specialty_area: str):
        # Call parent constructor
        super().__init__(code, description, base_rate)
        if not specialty_area or not specialty_area.strip():
            raise InvalidInputError("Specialty area is required.")
        self.specialty_area = specialty_area.strip()

    def calculate_total_cost(self, hours: int) -> float:
        # Polymorphic calculation: applies a 5% discount for sessions longer than 5 hours
        subtotal = self.base_rate * hours
        return subtotal * 0.95 if hours > 5 else subtotal


class Booking:
    """Represents a confirmed service reservation linked to a specific client."""

    def __init__(self, booking_id: int, client: Client, service: Service, hours: int):
        if hours <= 0:
            raise InvalidInputError("Booking duration must be at least 1 hour.")
        self.booking_id = booking_id
        self.client = client
        self.service = service
        self.hours = hours
        # Calculate final price dynamically using polymorphism
        self.total_cost = service.calculate_total_cost(hours)