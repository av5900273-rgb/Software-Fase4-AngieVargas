from datetime import datetime


class FileLogger:
    """Class responsible exclusively for logging system events and errors to a text file."""

    # Define the name of the log file where events and errors will be stored
    LOG_FILE = "events_errors_log.txt"

    @staticmethod
    def log(event_type: str, message: str) -> None:
        """Writes a timestamped entry to the log file without crashing the app on failure."""
        try:
            # Get the current date and time formatted as YYYY-MM-DD HH:MM:SS
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Build the log line with timestamp, event category, and description
            log_entry = f"[{timestamp}] [{event_type.upper()}] {message}\n"

            # Open the file in append mode ('a') with UTF-8 encoding and write the line
            with open(FileLogger.LOG_FILE, "a", encoding="utf-8") as file:
                file.write(log_entry)
        except Exception as error:
            # Print to terminal only if disk writing fails critically
            print(f"Critical error writing to log file: {error}")