from abc import ABC, abstractmethod
from typing import Optional
from exceptions import InvalidInputError, SoftwareFJError


class SystemEntity(ABC):
    """Abstract base class representing general identifiable entities in the system."""

    def __init__(self, entity_id: str):
        if not entity_id or not entity_id.strip():
            raise InvalidInputError("Entity ID cannot be empty.")
        self._entity_id = entity_id.strip()

    @property
    def entity_id(self) -> str:
        return self._entity_id

    @abstractmethod
    def get_summary(self) -> str:
        """Abstract method to return a formatted summary of the entity."""
        pass


class Client(SystemEntity):
    """Represents a client inheriting from SystemEntity with encapsulated personal data."""

    def __init__(self, client_id: str, full_name: str, email: str):
        super().__init__(client_id)
        self.full_name = full_name
        self.email = email

    @property
    def client_id(self) -> str:
        return self._entity_id

    @property
    def full_name(self) -> str:
        return self._full_name

    @full_name.setter
    def full_name(self, value: str) -> None:
        if not value or not value.strip():
            raise InvalidInputError("Client full name is required.")
        self._full_name = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if not value or "@" not in value or "." not in value:
            raise InvalidInputError("Invalid email address format.")
        self._email = value.strip()

    def get_summary(self) -> str:
        return f"Client [{self.client_id}]: {self.full_name} ({self.email})"

    def __str__(self) -> str:
        return f"{self.client_id} - {self.full_name} ({self.email})"


class Service(ABC):
    """Abstract base class defining the common structure for all Software FJ services."""

    def __init__(self, code: str, description: str, base_rate: float):
        if not code or not code.strip():
            raise InvalidInputError("Service code cannot be empty.")
        if not description or not description.strip():
            raise InvalidInputError("Service description cannot be empty.")
        if base_rate <= 0:
            raise InvalidInputError("Base rate must be greater than zero.")

        self._code = code.strip()
        self._description = description.strip()
        self._base_rate = float(base_rate)
        self.available = True

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
    def calculate_total_cost(
        self, hours: int, tax_rate: float = 0.0, discount_rate: float = 0.0
    ) -> float:
        """Overloaded/polymorphic cost calculation supporting optional taxes and discounts."""
        pass

    def _apply_tax_and_discount(
        self, subtotal: float, tax_rate: float, discount_rate: float
    ) -> float:
        """Helper method validating and applying optional tax and discount parameters."""
        if tax_rate < 0 or discount_rate < 0 or discount_rate > 1:
            raise InvalidInputError("Invalid tax or discount rate parameters.")
        discounted = subtotal * (1 - discount_rate)
        return discounted * (1 + tax_rate)

    def get_details(self) -> str:
        return f"[{self.code}] {self.description} - Base Rate: ${self.base_rate:.2f}/hr"


class RoomBooking(Service):
    """Derived class for meeting or conference room bookings."""

    def __init__(self, code: str, description: str, base_rate: float, capacity: int):
        super().__init__(code, description, base_rate)
        if capacity <= 0:
            raise InvalidInputError("Room capacity must be at least 1 person.")
        self.capacity = capacity

    def calculate_total_cost(
        self, hours: int, tax_rate: float = 0.0, discount_rate: float = 0.0
    ) -> float:
        if hours <= 0:
            raise InvalidInputError("Hours must be greater than zero.")
        subtotal = self.base_rate * hours
        if self.capacity > 20:
            subtotal *= 1.10
        return self._apply_tax_and_discount(subtotal, tax_rate, discount_rate)


class EquipmentRental(Service):
    """Derived class for technological or audiovisual equipment rentals."""

    def __init__(self, code: str, description: str, base_rate: float, equipment_type: str):
        super().__init__(code, description, base_rate)
        if not equipment_type or not equipment_type.strip():
            raise InvalidInputError("Equipment type is required.")
        self.equipment_type = equipment_type.strip()

    def calculate_total_cost(
        self, hours: int, tax_rate: float = 0.0, discount_rate: float = 0.0
    ) -> float:
        if hours <= 0:
            raise InvalidInputError("Hours must be greater than zero.")
        subtotal = (self.base_rate * hours) + 15.0
        return self._apply_tax_and_discount(subtotal, tax_rate, discount_rate)


class SpecializedConsulting(Service):
    """Derived class for specialized software and IT consulting services."""

    def __init__(self, code: str, description: str, base_rate: float, specialty_area: str):
        super().__init__(code, description, base_rate)
        if not specialty_area or not specialty_area.strip():
            raise InvalidInputError("Specialty area is required.")
        self.specialty_area = specialty_area.strip()

    def calculate_total_cost(
        self, hours: int, tax_rate: float = 0.0, discount_rate: float = 0.0
    ) -> float:
        if hours <= 0:
            raise InvalidInputError("Hours must be greater than zero.")
        subtotal = self.base_rate * hours
        if hours > 5:
            subtotal *= 0.95
        return self._apply_tax_and_discount(subtotal, tax_rate, discount_rate)


class Booking:
    """Represents a service booking with status management (Pending, Confirmed, Cancelled)."""

    def __init__(
        self,
        booking_id: int,
        client: Client,
        service: Service,
        hours: int,
        tax_rate: float = 0.0,
        discount_rate: float = 0.0,
    ):
        if hours <= 0:
            raise InvalidInputError("Booking duration must be at least 1 hour.")
        if not service.available:
            raise SoftwareFJError(f"Service '{service.code}' is currently unavailable.")

        self.booking_id = booking_id
        self.client = client
        self.service = service
        self.hours = hours
        self.status = "Pending"
        self.total_cost = service.calculate_total_cost(hours, tax_rate, discount_rate)

    def confirm(self) -> None:
        """Confirms a pending booking with strict state validation."""
        if self.status == "Cancelled":
            raise SoftwareFJError(f"Booking #{self.booking_id} cannot be confirmed because it is already Cancelled.")
        if self.status == "Confirmed":
            raise SoftwareFJError(f"Booking #{self.booking_id} is already Confirmed.")
        self.status = "Confirmed"

    def cancel(self) -> None:
        """Cancels an active booking with strict state validation."""
        if self.status == "Cancelled":
            raise SoftwareFJError(f"Booking #{self.booking_id} is already Cancelled.")
        self.status = "Cancelled"