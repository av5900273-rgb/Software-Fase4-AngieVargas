class SoftwareFJError(Exception):
    """Base custom exception for business logic and validation errors in Software FJ."""

    def __init__(self, message: str):
        # Pass the custom error message to the parent Exception class
        super().__init__(message)


class DuplicateRecordError(SoftwareFJError):
    """Raised when attempting to register an ID or code that already exists."""
    pass


class RecordNotFoundError(SoftwareFJError):
    """Raised when a requested client or service cannot be found in memory."""
    pass


class InvalidInputError(SoftwareFJError):
    """Raised when user inputs fail validation rules (empty fields, negative numbers, etc.)."""
    pass