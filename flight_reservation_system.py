import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time

# ==========================================================
# FLIGHT RESERVATION SYSTEM USING SEARCHING AND SORTING
# Searching : Linear Search, Binary Search
# Sorting   : Bubble, Selection, Insertion, Merge, Quick Sort
# ==========================================================

# HELPER FUNCTIONS
def to_minutes(t):
    """Convert 'HH:MM' into minutes after midnight."""
    h, m = t.split(":")
    return int(h) * 60 + int(m)


def calc_duration(dep, arr):
    """Flight duration in minutes (handles overnight flights)."""
    d = to_minutes(arr) - to_minutes(dep)
    if d <= 0:
        d += 24 * 60
    return d


def fmt_duration(minutes):
    return f"{minutes // 60}h {minutes % 60:02d}m"


def make_flight(no, airline, source, dest, dep, arr, price, seats):
    return {
        "no": no,
        "airline": airline,
        "source": source,
        "dest": dest,
        "dep": dep,
        "arr": arr,
        "duration": calc_duration(dep, arr),
        "price": price,
        "seats": seats,
    }


# SAMPLE FLIGHTS
flights = [
    make_flight("AI101", "Air India", "Pune", "Delhi", "06:30", "08:45", 5400, 40),
    make_flight("6E202", "IndiGo", "Pune", "Delhi", "09:15", "11:30", 4800, 35),
    make_flight("SG303", "SpiceJet", "Mumbai", "Delhi", "07:00", "09:10", 4500, 30),
    make_flight("UK404", "Vistara", "Mumbai", "Bangalore", "10:20", "12:05", 5100, 28),
    make_flight("AI505", "Air India", "Delhi", "Chennai", "13:45", "16:30", 6900, 45),
    make_flight("6E606", "IndiGo", "Pune", "Bangalore", "15:10", "16:40", 3900, 50),
    make_flight("SG707", "SpiceJet", "Nagpur", "Pune", "17:30", "18:50", 3600, 25),
    make_flight("UK808", "Vistara", "Delhi", "Mumbai", "19:00", "21:15", 5700, 32),
    make_flight("AI909", "Air India", "Bangalore", "Kolkata", "21:40", "00:10", 7200, 38),
    make_flight("6E110", "IndiGo", "Nagpur", "Mumbai", "05:50", "07:20", 3300, 42),
    make_flight("UK212", "Vistara", "Chennai", "Pune", "11:05", "13:00", 4200, 20),
    make_flight("SG314", "SpiceJet", "Kolkata", "Delhi", "08:25", "10:55", 6100, 36),
]

bookings = []
booking_counter = 1001


# SORTING ALGORITHMS
def bubble_sort(data, key):
    arr = data[:]
    comps = 0
    n = len(arr)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comps += 1
            if key(arr[j]) > key(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr, comps


def selection_sort(data, key):
    arr = data[:]
    comps = 0
    n = len(arr)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            comps += 1
            if key(arr[j]) < key(arr[min_index]):
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr, comps


def insertion_sort(data, key):
    arr = data[:]
    comps = 0
    for i in range(1, len(arr)):
        current = arr[i]
        j = i - 1
        while j >= 0:
            comps += 1
            if key(arr[j]) > key(current):
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = current
    return arr, comps


def merge_sort(data, key):
    comps = [0]

    def sort(a):
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left = sort(a[:mid])
        right = sort(a[mid:])
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            comps[0] += 1
            if key(left[i]) <= key(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    return sort(data[:]), comps[0]


def quick_sort(data, key):
    arr = data[:]
    comps = [0]

    def partition(low, high):
        pivot = key(arr[high])
        i = low - 1
        for j in range(low, high):
            comps[0] += 1
            if key(arr[j]) <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def qs(low, high):
        if low < high:
            p = partition(low, high)
            qs(low, p - 1)
            qs(p + 1, high)

    qs(0, len(arr) - 1)
    return arr, comps[0]


SORT_ALGORITHMS = {
    "Bubble Sort": bubble_sort,
    "Selection Sort": selection_sort,
    "Insertion Sort": insertion_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
}

SORT_KEYS = {
    "Price": lambda f: f["price"],
    "Departure Time": lambda f: to_minutes(f["dep"]),
    "Duration": lambda f: f["duration"],
    "Flight No": lambda f: f["no"],
}


# SEARCHING ALGORITHMS
def linear_search_flight(data, flight_no):
    """Check flights one by one. Returns (flight or None, comparisons)."""
    comps = 0
    for f in data:
        comps += 1
        if f["no"] == flight_no:
            return f, comps
    return None, comps


def binary_search_flight(data, flight_no):
    """Binary search needs sorted data, so flights are first sorted by Flight No."""
    sorted_data, _ = merge_sort(data, SORT_KEYS["Flight No"])
    low, high = 0, len(sorted_data) - 1
    comps = 0
    while low <= high:
        mid = (low + high) // 2
        comps += 1
        if sorted_data[mid]["no"] == flight_no:
            return sorted_data[mid], comps
        elif sorted_data[mid]["no"] < flight_no:
            low = mid + 1
        else:
            high = mid - 1
    return None, comps


def search_route(data, source, dest):
    """Linear search for all flights from source to destination."""
    result = []
    comps = 0
    for f in data:
        comps += 1
        if f["source"].lower() == source.lower() and f["dest"].lower() == dest.lower():
            result.append(f)
    return result, comps


def search_by_price(data, max_price):
    """Linear search for all flights costing up to max_price."""
    result = []
    comps = 0
    for f in data:
        comps += 1
        if f["price"] <= max_price:
            result.append(f)
    return result, comps


# GUI APPLICATION
class FlightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Reservation System - Searching and Sorting")
        self.root.geometry("1300x800")
        self.root.configure(bg="#f4f6f8")

        self.view = flights[:]
        self.info_var = tk.StringVar(value="Ready.")
        self.build_gui()
        self.refresh_flights(self.view)
        self.refresh_bookings()

    def build_gui(self):
        tk.Label(
            self.root, text="FLIGHT RESERVATION SYSTEM",
            font=("Arial", 22, "bold"), bg="#f4f6f8", fg="#1f3c88"
        ).pack(pady=8)
        tk.Label(
            self.root,
            text="Implementation using Searching (Linear, Binary) and Sorting "
                 "(Bubble, Selection, Insertion, Merge, Quick)",
            font=("Arial", 11), bg="#f4f6f8"
        ).pack()

        # Flight details
        fd = tk.LabelFrame(
            self.root, text="Flight Details (Add New Flight)",
            font=("Arial", 11, "bold"), bg="white", padx=10, pady=6
        )
        fd.pack(fill="x", padx=20, pady=(10, 4))

        labels = [
            "Flight No:", "Airline:", "Source:", "Destination:",
            "Departure (HH:MM):", "Arrival (HH:MM):", "Price (Rs.):", "Seats:"
        ]
        self.fd_entries = []
        for i, label in enumerate(labels):
            r, c = divmod(i, 4)
            tk.Label(fd, text=label, bg="white").grid(
                row=r, column=c * 2, padx=8, pady=5, sticky="e"
            )
            entry = tk.Entry(fd, width=18)
            entry.grid(row=r, column=c * 2 + 1, padx=8, pady=5)
            self.fd_entries.append(entry)

        (self.no_e, self.airline_e, self.src_e, self.dst_e,
         self.dep_e, self.arr_e, self.price_e, self.seats_e) = self.fd_entries

        tk.Button(fd, text="Add Flight", width=14, command=self.add_flight).grid(
            row=2, column=6, pady=4
        )
        tk.Button(fd, text="Clear", width=14, command=self.clear_flight_fields).grid(
            row=2, column=7, pady=4
        )

        # Search
        sf = tk.LabelFrame(
            self.root, text="Search Flights",
            font=("Arial", 11, "bold"), bg="white", padx=10, pady=6
        )
        sf.pack(fill="x", padx=20, pady=4)

        tk.Label(sf, text="Search By:", bg="white").grid(row=0, column=0, padx=8)
        self.search_by = ttk.Combobox(
            sf, state="readonly", width=30,
            values=[
                "Flight No (Linear Search)", "Flight No (Binary Search)",
                "Route (Linear Search)", "Price up to (Linear Search)"
            ]
        )
        self.search_by.current(0)
        self.search_by.grid(row=0, column=1, padx=8)

        tk.Label(sf, text="Value / Source:", bg="white").grid(row=0, column=2, padx=8)
        self.search_val = tk.Entry(sf, width=18)
        self.search_val.grid(row=0, column=3, padx=8)

        tk.Label(sf, text="Destination (route only):", bg="white").grid(
            row=0, column=4, padx=8
        )
        self.search_dst = tk.Entry(sf, width=18)
        self.search_dst.grid(row=0, column=5, padx=8)

        tk.Button(sf, text="Search", width=12, command=self.search).grid(
            row=0, column=6, padx=8
        )
        tk.Button(sf, text="Show All", width=12, command=self.show_all).grid(
            row=0, column=7, padx=8
        )

        # Sort
        so = tk.LabelFrame(
            self.root, text="Sort Flights",
            font=("Arial", 11, "bold"), bg="white", padx=10, pady=6
        )
        so.pack(fill="x", padx=20, pady=4)

        tk.Label(so, text="Sort By:", bg="white").grid(row=0, column=0, padx=8)
        self.sort_key = ttk.Combobox(
            so, state="readonly", width=18, values=list(SORT_KEYS)
        )
        self.sort_key.current(0)
        self.sort_key.grid(row=0, column=1, padx=8)

        tk.Label(so, text="Algorithm:", bg="white").grid(row=0, column=2, padx=8)
        self.sort_algo = ttk.Combobox(
            so, state="readonly", width=18, values=list(SORT_ALGORITHMS)
        )
        self.sort_algo.current(3)
        self.sort_algo.grid(row=0, column=3, padx=8)

        tk.Label(so, text="Order:", bg="white").grid(row=0, column=4, padx=8)
        self.sort_order = ttk.Combobox(
            so, state="readonly", width=14, values=["Ascending", "Descending"]
        )
        self.sort_order.current(0)
        self.sort_order.grid(row=0, column=5, padx=8)

        tk.Button(so, text="Sort", width=12, command=self.sort_flights).grid(
            row=0, column=6, padx=8
        )
        tk.Button(so, text="Reset Order", width=12, command=self.show_all).grid(
            row=0, column=7, padx=8
        )

        # Booking / cancellation
        bf = tk.LabelFrame(
            self.root, text="Ticket Booking / Cancellation",
            font=("Arial", 11, "bold"), bg="white", padx=10, pady=6
        )
        bf.pack(fill="x", padx=20, pady=4)

        tk.Label(bf, text="Flight No:", bg="white").grid(
            row=0, column=0, padx=8, pady=4
        )
        self.b_flight = tk.Entry(bf, width=14)
        self.b_flight.grid(row=0, column=1, padx=8)

        tk.Label(bf, text="Passenger Name:", bg="white").grid(row=0, column=2, padx=8)
        self.b_name = tk.Entry(bf, width=22)
        self.b_name.grid(row=0, column=3, padx=8)

        tk.Label(bf, text="Phone:", bg="white").grid(row=0, column=4, padx=8)
        self.b_phone = tk.Entry(bf, width=16)
        self.b_phone.grid(row=0, column=5, padx=8)

        tk.Label(bf, text="Seats:", bg="white").grid(row=0, column=6, padx=8)
        self.b_seats = tk.Entry(bf, width=6)
        self.b_seats.grid(row=0, column=7, padx=8)

        tk.Button(bf, text="Book Ticket", width=14, command=self.book_ticket).grid(
            row=0, column=8, padx=8
        )

        tk.Label(bf, text="Booking ID:", bg="white").grid(
            row=1, column=0, padx=8, pady=4
        )
        self.c_id = tk.Entry(bf, width=14)
        self.c_id.grid(row=1, column=1, padx=8)
        tk.Button(
            bf, text="Cancel Booking", width=14, command=self.cancel_booking
        ).grid(row=1, column=2, padx=8)
        tk.Button(
            bf, text="Clear", width=14, command=self.clear_booking_fields
        ).grid(row=1, column=3, padx=8)
        tk.Button(bf, text="Exit", width=14, command=self.root.destroy).grid(
            row=1, column=8, padx=8
        )

        # Flights table
        tf = tk.Frame(self.root)
        tf.pack(fill="both", expand=True, padx=20, pady=(6, 2))
        cols = (
            "Flight No", "Airline", "Source", "Destination", "Departure",
            "Arrival", "Duration", "Price (Rs.)", "Seats Left"
        )
        self.flight_table = ttk.Treeview(tf, columns=cols, show="headings", height=9)
        for col in cols:
            self.flight_table.heading(col, text=col)
            self.flight_table.column(col, width=110, anchor="center")
        scrollbar = ttk.Scrollbar(tf, orient="vertical", command=self.flight_table.yview)
        self.flight_table.configure(yscrollcommand=scrollbar.set)
        self.flight_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.flight_table.bind("<<TreeviewSelect>>", self.on_select_flight)

        # Result / information
        tk.Label(
            self.root, textvariable=self.info_var, font=("Arial", 10, "bold"),
            bg="#f4f6f8", fg="#1f3c88"
        ).pack(pady=2)

        # Bookings table
        tk.Label(
            self.root, text="Booked Tickets", font=("Arial", 11, "bold"),
            bg="#f4f6f8"
        ).pack()
        bt = tk.Frame(self.root)
        bt.pack(fill="x", padx=20, pady=(2, 8))
        bcols = ("Booking ID", "Flight No", "Passenger", "Phone", "Seats", "Total Fare (Rs.)")
        self.booking_table = ttk.Treeview(bt, columns=bcols, show="headings", height=4)
        for col in bcols:
            self.booking_table.heading(col, text=col)
            self.booking_table.column(col, width=150, anchor="center")
        self.booking_table.pack(fill="x")

    # TABLE REFRESH
    def refresh_flights(self, data):
        for row in self.flight_table.get_children():
            self.flight_table.delete(row)
        for f in data:
            self.flight_table.insert("", tk.END, values=(
                f["no"], f["airline"], f["source"], f["dest"], f["dep"],
                f["arr"], fmt_duration(f["duration"]), f["price"], f["seats"]
            ))

    def refresh_bookings(self):
        for row in self.booking_table.get_children():
            self.booking_table.delete(row)
        for b in bookings:
            self.booking_table.insert("", tk.END, values=(
                b["id"], b["flight"], b["name"], b["phone"], b["seats"], b["total"]
            ))

    def on_select_flight(self, _event):
        selected = self.flight_table.selection()
        if selected:
            flight_no = self.flight_table.item(selected[0])["values"][0]
            self.b_flight.delete(0, tk.END)
            self.b_flight.insert(0, str(flight_no))

    def show_all(self):
        self.view = flights[:]
        self.refresh_flights(self.view)
        self.info_var.set(f"Showing all {len(self.view)} flights in original order.")

    # ADD FLIGHT
    def add_flight(self):
        no = self.no_e.get().strip().upper()
        airline = self.airline_e.get().strip()
        source = self.src_e.get().strip().title()
        dest = self.dst_e.get().strip().title()
        dep = self.dep_e.get().strip()
        arr = self.arr_e.get().strip()

        if not no or not airline or not source or not dest:
            messagebox.showwarning("Missing Information", "Please fill all required fields.")
            return
        if source.lower() == dest.lower():
            messagebox.showerror("Error", "Source and destination cannot be the same.")
            return
        try:
            datetime.strptime(dep, "%H:%M")
            datetime.strptime(arr, "%H:%M")
        except ValueError:
            messagebox.showerror(
                "Error", "Enter times in HH:MM (24-hour) format, e.g. 09:30."
            )
            return
        try:
            price = int(self.price_e.get())
            seats = int(self.seats_e.get())
            if price <= 0 or seats <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Error", "Price and seats must be positive whole numbers."
            )
            return
        if any(f["no"] == no for f in flights):
            messagebox.showerror("Duplicate", "A flight with this number already exists.")
            return

        flight = make_flight(no, airline, source, dest, dep, arr, price, seats)
        flights.append(flight)
        self.view.append(flight)
        self.refresh_flights(self.view)
        self.clear_flight_fields()
        self.info_var.set(f"Flight {no} added successfully.")
        messagebox.showinfo("Success", f"Flight {no} added successfully.")

    def clear_flight_fields(self):
        for entry in self.fd_entries:
            entry.delete(0, tk.END)

    # SEARCH
    def search(self):
        mode = self.search_by.get()
        value = self.search_val.get().strip()
        if not value:
            messagebox.showwarning("Missing Information", "Enter a value to search.")
            return

        start = time.perf_counter()
        if mode.startswith("Flight No (Linear"):
            found, comps = linear_search_flight(flights, value.upper())
            result = [found] if found else []
            method = "Linear Search"
        elif mode.startswith("Flight No (Binary"):
            found, comps = binary_search_flight(flights, value.upper())
            result = [found] if found else []
            method = "Binary Search"
        elif mode.startswith("Route"):
            destination = self.search_dst.get().strip()
            if not destination:
                messagebox.showwarning(
                    "Missing Information", "Enter the destination as well."
                )
                return
            result, comps = search_route(flights, value, destination)
            method = "Linear Search (Route)"
        else:
            try:
                limit = int(value)
            except ValueError:
                messagebox.showerror("Error", "Enter the maximum price as a number.")
                return
            result, comps = search_by_price(flights, limit)
            method = "Linear Search (Price)"

        elapsed = (time.perf_counter() - start) * 1000
        self.view = result
        self.refresh_flights(self.view)
        self.info_var.set(
            f"{method}: {len(result)} flight(s) found | Comparisons: {comps} | "
            f"Time: {elapsed:.4f} ms"
        )
        if not result:
            messagebox.showerror("Not Found", "No matching flight was found.")

    # SORT
    def sort_flights(self):
        key_name = self.sort_key.get()
        algo_name = self.sort_algo.get()
        start = time.perf_counter()
        result, comps = SORT_ALGORITHMS[algo_name](flights, SORT_KEYS[key_name])
        elapsed = (time.perf_counter() - start) * 1000
        if self.sort_order.get() == "Descending":
            result.reverse()
        self.view = result
        self.refresh_flights(self.view)
        self.info_var.set(
            f"{algo_name} by {key_name} ({self.sort_order.get()}) | "
            f"Comparisons: {comps} | Time: {elapsed:.4f} ms"
        )

    # BOOK / CANCEL
    def book_ticket(self):
        global booking_counter
        flight_no = self.b_flight.get().strip().upper()
        name = self.b_name.get().strip()
        phone = self.b_phone.get().strip()

        if not flight_no or not name or not phone:
            messagebox.showwarning("Missing Information", "Please fill all booking fields.")
            return
        if not (phone.isdigit() and len(phone) == 10):
            messagebox.showerror("Error", "Phone number must contain exactly 10 digits.")
            return
        try:
            seats = int(self.b_seats.get())
            if seats <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Seats must be a positive whole number.")
            return

        flight, _ = linear_search_flight(flights, flight_no)
        if flight is None:
            messagebox.showerror("Not Found", "Flight number does not exist.")
            return
        if seats > flight["seats"]:
            messagebox.showerror(
                "Seats Unavailable",
                f"Only {flight['seats']} seat(s) are left on {flight_no}."
            )
            return

        flight["seats"] -= seats
        booking = {
            "id": f"BK{booking_counter}",
            "flight": flight_no,
            "name": name,
            "phone": phone,
            "seats": seats,
            "total": seats * flight["price"],
        }
        booking_counter += 1
        bookings.append(booking)

        self.refresh_flights(self.view)
        self.refresh_bookings()
        self.clear_booking_fields()
        self.info_var.set(f"Booking {booking['id']} confirmed.")
        messagebox.showinfo(
            "Booking Confirmed",
            f"Booking ID: {booking['id']}\nFlight: {flight_no}\n"
            f"Passenger: {name}\nSeats: {seats}\nTotal Fare: Rs. {booking['total']}"
        )

    def cancel_booking(self):
        booking_id = self.c_id.get().strip().upper()
        if not booking_id:
            messagebox.showwarning("Missing Information", "Enter the Booking ID.")
            return
        for booking in bookings:
            if booking["id"] == booking_id:
                flight, _ = linear_search_flight(flights, booking["flight"])
                if flight:
                    flight["seats"] += booking["seats"]
                bookings.remove(booking)
                self.refresh_flights(self.view)
                self.refresh_bookings()
                self.c_id.delete(0, tk.END)
                self.info_var.set(f"Booking {booking_id} cancelled.")
                messagebox.showinfo(
                    "Cancelled", f"Booking {booking_id} cancelled successfully."
                )
                return
        messagebox.showerror("Not Found", "Booking ID not found.")

    def clear_booking_fields(self):
        for entry in (self.b_flight, self.b_name, self.b_phone, self.b_seats, self.c_id):
            entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    FlightApp(root)
    root.mainloop()
