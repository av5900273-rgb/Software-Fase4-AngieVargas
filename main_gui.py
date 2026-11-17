import tkinter as tk
from tkinter import ttk, messagebox
from manager import ManagementSystem
from exceptions import SoftwareFJError
from logger import FileLogger


class SoftwareFJApp:
    """Main graphical user interface built with Tkinter in English for Software FJ."""

    def __init__(self, root: tk.Tk):
        # Configure main application window
        self.root = root
        self.root.title("Software FJ - Service & Booking Management System")
        self.root.geometry("820x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#F4F6F9")

        # Initialize the core management system
        self.system = ManagementSystem()

        # Build UI widgets and load initial table data
        self._setup_styles()
        self._build_ui()
        self._refresh_tables()

    def _setup_styles(self) -> None:
        """Configures custom visual styles for tabs, buttons, and tables."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#F4F6F9", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[15, 8])
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#2C3E50", foreground="white")
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=26)

    def _build_ui(self) -> None:
        """Creates the header banner and tabbed layout for Clients, Bookings, and Catalog."""
        # Top Header Banner
        header = tk.Frame(self.root, bg="#1B4F72", height=65)
        header.pack(fill="x")
        title_label = tk.Label(
            header,
            text="SOFTWARE FJ - SERVICE & BOOKING MANAGEMENT",
            font=("Segoe UI", 14, "bold"),
            bg="#1B4F72",
            fg="white",
        )
        title_label.pack(pady=18)

        # Tabbed Container
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        # Create three main tabs
        self.tab_clients = tk.Frame(self.notebook, bg="white")
        self.tab_bookings = tk.Frame(self.notebook, bg="white")
        self.tab_services = tk.Frame(self.notebook, bg="white")

        self.notebook.add(self.tab_clients, text="1. Client Management")
        self.notebook.add(self.tab_bookings, text="2. Service Bookings")
        self.notebook.add(self.tab_services, text="3. Service Catalog")

        # Populate each tab
        self._build_clients_tab()
        self._build_bookings_tab()
        self._build_services_tab()

    # =========================================================================
    # TAB 1: CLIENT REGISTRATION & LIST
    # =========================================================================
    def _build_clients_tab(self) -> None:
        """Builds the form and table for registering and viewing clients."""
        form_frame = tk.LabelFrame(
            self.tab_clients, text=" Register New Client ", font=("Segoe UI", 10, "bold"), bg="white", padx=15, pady=15
        )
        form_frame.pack(fill="x", padx=15, pady=15)

        # Client ID input
        tk.Label(form_frame, text="Client ID:", font=("Segoe UI", 9), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_client_id = tk.Entry(form_frame, width=22, font=("Segoe UI", 10))
        self.entry_client_id.grid(row=0, column=1, padx=10, pady=5)

        # Full Name input
        tk.Label(form_frame, text="Full Name:", font=("Segoe UI", 9), bg="white").grid(row=0, column=2, sticky="w", pady=5)
        self.entry_client_name = tk.Entry(form_frame, width=28, font=("Segoe UI", 10))
        self.entry_client_name.grid(row=0, column=3, padx=10, pady=5)

        # Email input
        tk.Label(form_frame, text="Email Address:", font=("Segoe UI", 9), bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_client_email = tk.Entry(form_frame, width=22, font=("Segoe UI", 10))
        self.entry_client_email.grid(row=1, column=1, padx=10, pady=5)

        # Register Button
        btn_register = tk.Button(
            form_frame,
            text="Register Client",
            font=("Segoe UI", 9, "bold"),
            bg="#2874A6",
            fg="white",
            cursor="hand2",
            padx=15,
            pady=4,
            command=self._handle_register_client,
        )
        btn_register.grid(row=1, column=3, sticky="e", padx=10, pady=5)

        # Clients Table
        table_frame = tk.Frame(self.tab_clients, bg="white")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        columns = ("id", "name", "email")
        self.tree_clients = ttk.Treeview(table_frame, columns=columns, show="headings", height=11)
        self.tree_clients.heading("id", text="Client ID")
        self.tree_clients.heading("name", text="Full Name")
        self.tree_clients.heading("email", text="Email Address")

        self.tree_clients.column("id", width=140, anchor="center")
        self.tree_clients.column("name", width=300)
        self.tree_clients.column("email", width=280)
        self.tree_clients.pack(fill="both", expand=True)

    # =========================================================================
    # TAB 2: BOOKING CREATION & HISTORY
    # =========================================================================
    def _build_bookings_tab(self) -> None:
        """Builds the form and table for creating and listing service bookings."""
        form_frame = tk.LabelFrame(
            self.tab_bookings, text=" Create New Booking ", font=("Segoe UI", 10, "bold"), bg="white", padx=15, pady=15
        )
        form_frame.pack(fill="x", padx=15, pady=15)

        # Client ID input
        tk.Label(form_frame, text="Client ID:", font=("Segoe UI", 9), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_book_client = tk.Entry(form_frame, width=20, font=("Segoe UI", 10))
        self.entry_book_client.grid(row=0, column=1, padx=10, pady=5)

        # Service Code input
        tk.Label(form_frame, text="Service Code:", font=("Segoe UI", 9), bg="white").grid(row=0, column=2, sticky="w", pady=5)
        self.entry_book_service = tk.Entry(form_frame, width=20, font=("Segoe UI", 10))
        self.entry_book_service.grid(row=0, column=3, padx=10, pady=5)

        # Duration (Hours) input
        tk.Label(form_frame, text="Duration (Hours):", font=("Segoe UI", 9), bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_book_hours = tk.Entry(form_frame, width=20, font=("Segoe UI", 10))
        self.entry_book_hours.grid(row=1, column=1, padx=10, pady=5)

        # Create Booking Button
        btn_book = tk.Button(
            form_frame,
            text="Confirm Booking",
            font=("Segoe UI", 9, "bold"),
            bg="#1E8449",
            fg="white",
            cursor="hand2",
            padx=15,
            pady=4,
            command=self._handle_create_booking,
        )
        btn_book.grid(row=1, column=3, sticky="e", padx=10, pady=5)

        # Bookings Table
        table_frame = tk.Frame(self.tab_bookings, bg="white")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        columns = ("id", "client", "service", "hours", "total")
        self.tree_bookings = ttk.Treeview(table_frame, columns=columns, show="headings", height=11)
        self.tree_bookings.heading("id", text="Booking #")
        self.tree_bookings.heading("client", text="Client")
        self.tree_bookings.heading("service", text="Service")
        self.tree_bookings.heading("hours", text="Hours")
        self.tree_bookings.heading("total", text="Total Cost ($)")

        self.tree_bookings.column("id", width=80, anchor="center")
        self.tree_bookings.column("client", width=200)
        self.tree_bookings.column("service", width=240)
        self.tree_bookings.column("hours", width=80, anchor="center")
        self.tree_bookings.column("total", width=120, anchor="e")
        self.tree_bookings.pack(fill="both", expand=True)

    # =========================================================================
    # TAB 3: AVAILABLE SERVICES CATALOG
    # =========================================================================
    def _build_services_tab(self) -> None:
        """Displays the catalog of polymorphic services offered by Software FJ."""
        info_label = tk.Label(
            self.tab_services,
            text="Available Services & Polymorphic Pricing Rules",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#2C3E50",
        )
        info_label.pack(anchor="w", padx=15, pady=(15, 5))

        table_frame = tk.Frame(self.tab_services, bg="white")
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("code", "category", "description", "rate")
        self.tree_services = ttk.Treeview(table_frame, columns=columns, show="headings", height=13)
        self.tree_services.heading("code", text="Code")
        self.tree_services.heading("category", text="Service Category")
        self.tree_services.heading("description", text="Description")
        self.tree_services.heading("rate", text="Base Rate ($/hr)")

        self.tree_services.column("code", width=90, anchor="center")
        self.tree_services.column("category", width=170)
        self.tree_services.column("description", width=330)
        self.tree_services.column("rate", width=130, anchor="e")
        self.tree_services.pack(fill="both", expand=True)

    # =========================================================================
    # EVENT HANDLERS WITH STRICT EXCEPTION HANDLING
    # =========================================================================
    def _handle_register_client(self) -> None:
        """Handles client registration button click with error dialogs and logging."""
        try:
            client_id = self.entry_client_id.get()
            full_name = self.entry_client_name.get()
            email = self.entry_client_email.get()

            self.system.register_client(client_id, full_name, email)
            messagebox.showinfo("Success", "Client registered successfully!")

            # Clear input fields and refresh table
            self.entry_client_id.delete(0, tk.END)
            self.entry_client_name.delete(0, tk.END)
            self.entry_client_email.delete(0, tk.END)
            self._refresh_tables()

        except SoftwareFJError as business_err:
            messagebox.showwarning("Validation Error", str(business_err))
        except Exception as unexpected_err:
            FileLogger.log("CRITICAL", f"Unexpected GUI error during client registration: {unexpected_err}")
            messagebox.showerror("System Error", f"An unexpected error occurred: {unexpected_err}")

    def _handle_create_booking(self) -> None:
        """Handles booking creation button click, validating integer hours safely."""
        try:
            client_id = self.entry_book_client.get()
            service_code = self.entry_book_service.get()
            hours_text = self.entry_book_hours.get().strip()

            # Validate numeric input before calling overloaded method
            if not hours_text.isdigit():
                FileLogger.log("ERROR", f"Invalid non-numeric hours input: '{hours_text}'")
                raise ValueError("Duration (Hours) must be a valid positive whole number.")

            hours = int(hours_text)
            booking = self.system.create_booking(client_id, service_code, hours)

            messagebox.showinfo(
                "Booking Confirmed",
                f"Booking #{booking.booking_id} created!\nTotal Cost: ${booking.total_cost:.2f}",
            )

            # Clear fields and update bookings table
            self.entry_book_client.delete(0, tk.END)
            self.entry_book_service.delete(0, tk.END)
            self.entry_book_hours.delete(0, tk.END)
            self._refresh_tables()

        except (SoftwareFJError, ValueError) as validation_err:
            messagebox.showwarning("Booking Error", str(validation_err))
        except Exception as unexpected_err:
            FileLogger.log("CRITICAL", f"Unexpected GUI error during booking creation: {unexpected_err}")
            messagebox.showerror("System Error", f"An unexpected error occurred: {unexpected_err}")

    def _refresh_tables(self) -> None:
        """Reloads all Treeview tables with the latest in-memory data."""
        # Refresh Clients Table
        for item in self.tree_clients.get_children():
            self.tree_clients.delete(item)
        for client in self.system.get_all_clients():
            self.tree_clients.insert("", tk.END, values=(client.client_id, client.full_name, client.email))

        # Refresh Bookings Table
        for item in self.tree_bookings.get_children():
            self.tree_bookings.delete(item)
        for booking in self.system.get_all_bookings():
            self.tree_bookings.insert(
                "",
                tk.END,
                values=(
                    f"#{booking.booking_id}",
                    booking.client.full_name,
                    booking.service.description,
                    booking.hours,
                    f"${booking.total_cost:.2f}",
                ),
            )

        # Refresh Services Catalog Table
        for item in self.tree_services.get_children():
            self.tree_services.delete(item)
        for service in self.system.get_all_services():
            self.tree_services.insert(
                "",
                tk.END,
                values=(
                    service.code,
                    service.__class__.__name__,
                    service.description,
                    f"${service.base_rate:.2f}",
                ),
            )


if __name__ == "__main__":
    # Launch the Tkinter application
    root = tk.Tk()
    app = SoftwareFJApp(root)
    root.mainloop()