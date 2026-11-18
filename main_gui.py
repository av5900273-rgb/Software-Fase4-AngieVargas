import tkinter as tk
from tkinter import ttk, messagebox
from manager import ManagementSystem
from exceptions import SoftwareFJError
from logger import FileLogger


class SoftwareFJApp:
    """Main graphical user interface built with Tkinter in English for Software FJ."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Software FJ - Integral Service & Booking Management System")
        self.root.geometry("860x640")
        self.root.resizable(False, False)
        self.root.configure(bg="#F4F6F9")

        self.system = ManagementSystem()

        self._setup_styles()
        self._build_ui()
        self._refresh_tables()

    def _setup_styles(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#F4F6F9", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=(12, 6))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#2C3E50", foreground="white")
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=26)

    def _build_ui(self) -> None:
        # Top Header Banner with Simulation Button
        header = tk.Frame(self.root, bg="#1B4F72", height=65)
        header.pack(fill="x")

        title_label = tk.Label(
            header,
            text="SOFTWARE FJ - SERVICE & BOOKING MANAGEMENT",
            font=("Segoe UI", 13, "bold"),
            bg="#1B4F72",
            fg="white",
        )
        title_label.pack(side="left", padx=20, pady=18)

        btn_sim = tk.Button(
            header,
            text="Run 10-Op Simulation",
            font=("Segoe UI", 9, "bold"),
            bg="#D68910",
            fg="white",
            cursor="hand2",
            padx=12,
            pady=5,
            command=self._handle_run_simulation,
        )
        btn_sim.pack(side="right", padx=20, pady=15)

        # Tabbed Container
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=15)

        self.tab_clients = tk.Frame(self.notebook, bg="white")
        self.tab_bookings = tk.Frame(self.notebook, bg="white")
        self.tab_services = tk.Frame(self.notebook, bg="white")

        self.notebook.add(self.tab_clients, text="1. Client Management")
        self.notebook.add(self.tab_bookings, text="2. Service Bookings")
        self.notebook.add(self.tab_services, text="3. Service Catalog")

        self._build_clients_tab()
        self._build_bookings_tab()
        self._build_services_tab()

    # =========================================================================
    # TAB 1: CLIENT REGISTRATION & LIST
    # =========================================================================
    def _build_clients_tab(self) -> None:
        form_frame = tk.LabelFrame(
            self.tab_clients, text=" Register New Client ", font=("Segoe UI", 10, "bold"), bg="white", padx=15, pady=15
        )
        form_frame.pack(fill="x", padx=15, pady=15)

        tk.Label(form_frame, text="Client ID:", font=("Segoe UI", 9), bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_client_id = tk.Entry(form_frame, width=22, font=("Segoe UI", 10))
        self.entry_client_id.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Full Name:", font=("Segoe UI", 9), bg="white").grid(row=0, column=2, sticky="w", pady=5)
        self.entry_client_name = tk.Entry(form_frame, width=28, font=("Segoe UI", 10))
        self.entry_client_name.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(form_frame, text="Email Address:", font=("Segoe UI", 9), bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_client_email = tk.Entry(form_frame, width=22, font=("Segoe UI", 10))
        self.entry_client_email.grid(row=1, column=1, padx=10, pady=5)

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

        table_frame = tk.Frame(self.tab_clients, bg="white")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        columns = ("id", "name", "email")
        self.tree_clients = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.tree_clients.heading("id", text="Client ID")
        self.tree_clients.heading("name", text="Full Name")
        self.tree_clients.heading("email", text="Email Address")

        self.tree_clients.column("id", width=140, anchor="center")
        self.tree_clients.column("name", width=320)
        self.tree_clients.column("email", width=300)
        self.tree_clients.pack(fill="both", expand=True)

    # =========================================================================
    # TAB 2: BOOKING CREATION, CANCELLATION & HISTORY
    # =========================================================================
    def _build_bookings_tab(self) -> None:
        form_frame = tk.LabelFrame(
            self.tab_bookings, text=" Create or Manage Bookings ", font=("Segoe UI", 10, "bold"), bg="white", padx=15, pady=12
        )
        form_frame.pack(fill="x", padx=15, pady=12)

        tk.Label(form_frame, text="Client ID:", font=("Segoe UI", 9), bg="white").grid(row=0, column=0, sticky="w", pady=4)
        self.entry_book_client = tk.Entry(form_frame, width=16, font=("Segoe UI", 10))
        self.entry_book_client.grid(row=0, column=1, padx=8, pady=4)

        tk.Label(form_frame, text="Service Code:", font=("Segoe UI", 9), bg="white").grid(row=0, column=2, sticky="w", pady=4)
        self.entry_book_service = tk.Entry(form_frame, width=16, font=("Segoe UI", 10))
        self.entry_book_service.grid(row=0, column=3, padx=8, pady=4)

        tk.Label(form_frame, text="Hours:", font=("Segoe UI", 9), bg="white").grid(row=0, column=4, sticky="w", pady=4)
        self.entry_book_hours = tk.Entry(form_frame, width=10, font=("Segoe UI", 10))
        self.entry_book_hours.grid(row=0, column=5, padx=8, pady=4)

        tk.Label(form_frame, text="Tax (%):", font=("Segoe UI", 9), bg="white").grid(row=1, column=0, sticky="w", pady=4)
        self.entry_book_tax = tk.Entry(form_frame, width=16, font=("Segoe UI", 10))
        self.entry_book_tax.insert(0, "0")
        self.entry_book_tax.grid(row=1, column=1, padx=8, pady=4)

        tk.Label(form_frame, text="Discount (%):", font=("Segoe UI", 9), bg="white").grid(row=1, column=2, sticky="w", pady=4)
        self.entry_book_discount = tk.Entry(form_frame, width=16, font=("Segoe UI", 10))
        self.entry_book_discount.insert(0, "0")
        self.entry_book_discount.grid(row=1, column=3, padx=8, pady=4)

        btn_book = tk.Button(
            form_frame,
            text="Confirm Booking",
            font=("Segoe UI", 9, "bold"),
            bg="#1E8449",
            fg="white",
            cursor="hand2",
            padx=12,
            pady=4,
            command=self._handle_create_booking,
        )
        btn_book.grid(row=1, column=4, columnspan=2, sticky="e", padx=8, pady=4)

        # Bookings Table
        table_frame = tk.Frame(self.tab_bookings, bg="white")
        table_frame.pack(fill="both", expand=True, padx=15, pady=(0, 8))

        columns = ("id", "client", "service", "hours", "status", "total")
        self.tree_bookings = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        self.tree_bookings.heading("id", text="ID")
        self.tree_bookings.heading("client", text="Client")
        self.tree_bookings.heading("service", text="Service")
        self.tree_bookings.heading("hours", text="Hours")
        self.tree_bookings.heading("status", text="Status")
        self.tree_bookings.heading("total", text="Total ($)")

        self.tree_bookings.column("id", width=55, anchor="center")
        self.tree_bookings.column("client", width=185)
        self.tree_bookings.column("service", width=230)
        self.tree_bookings.column("hours", width=65, anchor="center")
        self.tree_bookings.column("status", width=100, anchor="center")
        self.tree_bookings.column("total", width=110, anchor="e")
        self.tree_bookings.pack(fill="both", expand=True)

        # Cancel Booking Action Bar
        action_bar = tk.Frame(self.tab_bookings, bg="white")
        action_bar.pack(fill="x", padx=15, pady=(0, 12))

        btn_cancel = tk.Button(
            action_bar,
            text="Cancel Selected Booking",
            font=("Segoe UI", 9, "bold"),
            bg="#C0392B",
            fg="white",
            cursor="hand2",
            padx=12,
            pady=4,
            command=self._handle_cancel_booking,
        )
        btn_cancel.pack(side="right")

    # =========================================================================
    # TAB 3: AVAILABLE SERVICES CATALOG
    # =========================================================================
    def _build_services_tab(self) -> None:
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
        self.tree_services.column("category", width=180)
        self.tree_services.column("description", width=350)
        self.tree_services.column("rate", width=130, anchor="e")
        self.tree_services.pack(fill="both", expand=True)

    # =========================================================================
    # EVENT HANDLERS
    # =========================================================================
    def _handle_register_client(self) -> None:
        try:
            client_id = self.entry_client_id.get()
            full_name = self.entry_client_name.get()
            email = self.entry_client_email.get()

            self.system.register_client(client_id, full_name, email)
            messagebox.showinfo("Success", "Client registered successfully!")

            self.entry_client_id.delete(0, tk.END)
            self.entry_client_name.delete(0, tk.END)
            self.entry_client_email.delete(0, tk.END)
            self._refresh_tables()
        except SoftwareFJError as business_err:
            messagebox.showwarning("Validation Error", str(business_err))
        except Exception as unexpected_err:
            FileLogger.log("CRITICAL", f"Unexpected GUI error: {unexpected_err}")
            messagebox.showerror("System Error", f"An unexpected error occurred: {unexpected_err}")

    def _handle_create_booking(self) -> None:
        try:
            client_id = self.entry_book_client.get()
            service_code = self.entry_book_service.get()
            hours_text = self.entry_book_hours.get().strip()

            if not hours_text.isdigit():
                FileLogger.log("ERROR", f"Invalid non-numeric hours input: '{hours_text}'")
                raise ValueError("Duration (Hours) must be a valid positive whole number.")

            hours = int(hours_text)
            tax_rate = float(self.entry_book_tax.get().strip() or 0) / 100.0
            discount_rate = float(self.entry_book_discount.get().strip() or 0) / 100.0

            booking = self.system.create_booking(client_id, service_code, hours, tax_rate, discount_rate)
            messagebox.showinfo(
                "Booking Confirmed",
                f"Booking #{booking.booking_id} ({booking.status}) created!\nTotal Cost: ${booking.total_cost:.2f}",
            )

            self.entry_book_client.delete(0, tk.END)
            self.entry_book_service.delete(0, tk.END)
            self.entry_book_hours.delete(0, tk.END)
            self._refresh_tables()
        except (SoftwareFJError, ValueError) as validation_err:
            messagebox.showwarning("Booking Error", str(validation_err))
        except Exception as unexpected_err:
            FileLogger.log("CRITICAL", f"Unexpected GUI error: {unexpected_err}")
            messagebox.showerror("System Error", f"An unexpected error occurred: {unexpected_err}")

    def _handle_cancel_booking(self) -> None:
        try:
            selected = self.tree_bookings.selection()
            if not selected:
                raise SoftwareFJError("Please select a booking from the table to cancel.")
            item_values = self.tree_bookings.item(selected[0], "values")
            booking_id = int(str(item_values[0]).replace("#", ""))
            self.system.cancel_booking(booking_id)
            messagebox.showinfo("Booking Cancelled", f"Booking #{booking_id} has been cancelled.")
            self._refresh_tables()
        except SoftwareFJError as err:
            messagebox.showwarning("Cancellation Error", str(err))

    def _handle_run_simulation(self) -> None:
        summary = self.system.run_10_operations_simulation()
        self._refresh_tables()
        messagebox.showinfo("10-Operation Simulation Completed", summary)

    def _refresh_tables(self) -> None:
        for item in self.tree_clients.get_children():
            self.tree_clients.delete(item)
        for client in self.system.get_all_clients():
            self.tree_clients.insert("", tk.END, values=(client.client_id, client.full_name, client.email))

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
                    booking.status,
                    f"${booking.total_cost:.2f}",
                ),
            )

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
    root = tk.Tk()
    app = SoftwareFJApp(root)
    root.mainloop()

        

