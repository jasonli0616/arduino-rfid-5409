import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog

import threading
import keyboard

from . import arduino
from . import database


class GUI(tkinter.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("400x400")
        self.title("Arduino RFID 5409")

        self.__draw_select_port()

    def __draw_select_port(self):
        """Draw port selection components to the window."""

        # Store elements
        self.select_port_elements = []

        # Title
        title = ttk.Label(self, text="Select a port")
        self.select_port_elements.append(title)

        # Dropdown
        self.port_value = tkinter.StringVar(self)
        self.select_port = ttk.OptionMenu(self, self.port_value)
        self.__refresh_port_options()
        self.select_port_elements.append(self.select_port)

        # Refresh
        refresh_button = ttk.Button(
            self, text="Refresh ports", command=self.__refresh_port_options
        )
        self.select_port_elements.append(refresh_button)

        # Submit to thread
        submit_button = ttk.Button(
            self, text="Connect", command=self.__create_program_thread
        )
        self.select_port_elements.append(submit_button)

        for element in self.select_port_elements:
            element.pack()

    def __refresh_port_options(self):
        """Checks the ports, and updates the list."""
        self.select_port.set_menu("Select a port", *arduino.get_ports())

    def __create_program_thread(self):
        """
        Create a new thread that handles most of the program.
        Checks the port, and handles user scanning.
        """
        thread = threading.Thread(target=self.__submit_port)
        thread.start()

    def __submit_port(self):
        """
        Test the port, and notify user using dialog.

        If the port is successful/correct, it will start waiting for UID from Arduino.
        """
        port = self.port_value.get()
        try:
            connection = arduino.connect(port)
            messagebox.showinfo("SUCCESS", "Successful connection. Ready to scan.")

            # Wait for scan in thread
            self.__wait_for_uid(connection)

        except FileNotFoundError as err:
            messagebox.showerror(
                "ERROR",
                "Port is invalid. Try refreshing or selecting a different port.",
            )
        except Exception as err:
            messagebox.showerror("ERROR", err)

    def __wait_for_uid(self, connection):
        """
        Remove elements from the window.

        Wait for a UID from the Arduino.

        Creates new user, or types student ID.
        """

        # Remove elements from window
        for element in self.select_port_elements:
            element.destroy()

        # Add elements
        text = ttk.Label(
            self,
            text=f"Connected to {connection.port}.\nRestart program to connect to another port.",
        )
        text.pack()

        # Connect to database
        db = database.Database()

        # Wait for UID
        while True:
            read = connection.readline().decode().strip()
            if read.startswith("SCAN: "):
                # Receive UID
                uid = read.removeprefix("SCAN: ")
                student_id = db.get_student_id(uid)

                # New user
                if not student_id:
                    self.__ask_student_id(db, uid)

                else:
                    keyboard.write(student_id)
                    keyboard.press_and_release("enter")

    def __ask_student_id(self, db, uid):
        """
        Creates elements for user to enter student ID.
        """

        elements = []

        text = ttk.Label(self, text="\n\nCreate new user.\nEnter new student ID:")
        elements.append(text)

        entry = ttk.Entry(self)
        elements.append(entry)

        submit = ttk.Button(
            self,
            text="Submit student ID",
            command=lambda: self.__create_student(db, uid, entry.get(), elements),
        )
        elements.append(submit)

        for element in elements:
            element.pack()

    def __create_student(self, db, uid, student_id, destroy_elements):
        """Give the database the necessary data to create a new user."""
        if student_id:
            # Student ID already exists
            if db.get_uid(student_id):
                messagebox.showerror(
                    "ERROR", "ERROR: Student ID already exists in database."
                )
            else:
                db.create_new_user(uid, student_id)
                messagebox.showinfo(
                    "SUCCESS", "SUCCESS: User created. Scan again to use."
                )

        for element in destroy_elements:
            element.destroy()
